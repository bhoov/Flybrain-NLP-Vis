import yaml
import os
import numpy as np
from tokenizer import GensimTokenizer
from pathlib import Path
from functools import cached_property
from cachetools import cached, LRUCache
from typing import *


class Biohasher:
    """A class wrapper around a tokenizer, stop words, and synapse weights for hashing words"""

    def __init__(self, fname):
        ref_dir = Path(fname).parent
        with open(fname, "r") as fp:
            self.conf = yaml.load(fp, Loader=yaml.FullLoader)

        if "phrases" in self.conf.keys():
            phrases = ref_dir / self.conf["phrases"]
        else:
            phrases = None

        if "stop_words" in self.conf.keys():
            stop_words = ref_dir / self.conf["stop_words"]
        else:
            stop_words = None

        self.files = {
            "tokenizer": ref_dir / self.conf["tokenizer"],
            "phrases": phrases,
            "synapses": ref_dir / self.conf["synapses"],
            "stop_words": stop_words,
        }

    @cached_property
    def synapses(self):
        print("Loading synapses...")
        syn = np.load(self.files["synapses"])

        # Don't Normalize -- make it consistent with how the corpus was processed
        # K, N = syn.shape
        # prec = 1.0e-16
        # nc = np.sqrt(np.sum(syn ** 2, axis=1)).reshape(K, 1)
        # syn = syn / np.tile(nc + prec, (1, N))
        return syn

    @cached_property
    def tokenizer(self):
        print("Loading Tokenizer...")
        return GensimTokenizer.from_file(self.files["tokenizer"], self.files["phrases"])

    @cached_property
    def stop_words(self):
        """Words that are intentionally not learned by the model"""
        print("Loading stop words...")
        return set(np.load(self.files["stop_words"]))

    @cached_property
    def n_vocab(self):
        return self.tokenizer.n_vocab()

    def make_sentence_vector(self, token_ids, targ_idx=None, targ_coef=50, return_n_context=False, norm_by_context=False):
        """Create the input for the synapses given the token ids
        
        Args:
            token_ids: Tokenized input
            targ_idx: Which index to treat as the target index. Must be [0, len(token_ids))
            targ_coef: Force the target index to have this value
            return_n_context: Get information about the number of context tokens 
            norm_by_context: Set target value to number of context. Overrides other settings.
        """
        H, N = self.synapses.shape
        sentence = np.zeros((N,), dtype=np.int8)
        vocab = self.tokenizer.dictionary.keys()

        # Assign context
        n_context = 0
        for i, t in enumerate(token_ids):
            if i != targ_idx:
                if t in vocab and t not in self.stop_words:
                    n_context += 1
                    sentence[t] += 1

        # Assign target
        if norm_by_context: 
            target_value = n_context
        else:
            target_value = targ_coef

        if targ_idx is not None:
            target = token_ids[targ_idx]
            if target not in self.stop_words:
                sentence[self.n_vocab + target] = target_value

        if return_n_context:
            out = (sentence, n_context)
        else:
            out = sentence

        return out


    def get_hash_from_token_ids(self, token_ids: List[int], idx: Union[int, None], hash_length: int):
        """Get hashcode from a set of encoded tokens, selecting the index to use as the target word
        
        Args:
            token_ids: Encoded tokens of length N
            idx: Target index to create a hash code for. If None, create a hash of the whole N-Gram.
            hash_length: Number of non-zero units in the hash code. Alternatively, number of neurons to accept for hashing

        Returns:
            {
                hash: Desired hash code
                activated_neurons: Which neurons fired
                activations: 
                context_attentions: Synapse weights for each fired neuron for the context words
                target_attentions: Synapse weights for each fired neuron for the target word
            }
        """
        H, N = self.synapses.shape

        sentence, n_context = self.make_sentence_vector(token_ids, idx, return_n_context=True)

        act = np.dot(self.synapses, sentence)
        i_sorted = np.argsort(-act)
        act_sort = act[i_sorted]
        thr = (act_sort[hash_length - 1] + act_sort[hash_length]) / 2.0
        binary = act > thr

        # Extract attentions
        activated_neurons = i_sorted[:hash_length]
        context_ids = token_ids.copy()
        context_attentions = self.synapses[activated_neurons][:, context_ids].copy()

        if idx is not None:
            target_id = token_ids[idx]
            target_attentions = self.synapses[activated_neurons][:, self.n_vocab + target_id]
            context_attentions[:, idx] = n_context * target_attentions
        else:
            target_id = None
            target_attentions = None

        return {
            "hash": binary.flatten().astype(np.int8),# , attentions
            "activated_neurons": activated_neurons,
            "activations": act,
            "context_attentions": context_attentions,
            "target_attentions": target_attentions,
        }
            
    def get_hash_from_tokens(self, tokens, targ_token, hash_length):
        """Get hash from tokens"""
        token_ids = self.tokenizer.tokens2ids(tokens)
        targ = self.tokenizer.token2id(targ_token)

        try:
            idx = token_ids.index(targ)
        except ValueError as e:
            raise ValueError(f"Specified target token '{targ_token}' not found in '{tokens}'")

        return self.get_hash_from_token_ids(token_ids, idx, hash_length)


    def get_hash_from_string(self, string, targ_word, hash_length):
        """Hash the target word from the string
        
        Examples:
            >>> string1 = 'money in bank checking account'
            >>> out = project.get_hash_from_string(string1, "bank", 32)
        """
        tokens = self.tokenizer.encode(string)
        targ = self.tokenizer.encode(targ_word)[0]

        try:
            idx = tokens.index(targ)
        except ValueError as e:
            raise ValueError(f"Specified target word '{targ_word}' not found in '{self.tokenizer.decode(tokens)}'")

        return self.get_hash_from_token_ids(tokens, idx, hash_length)


    def get_k_neighbors(self, query: np.ndarray, k: int, hash_length: int) -> np.ndarray:
        """Get k nearest context independent codes from query
        
        Args:
            query: Hash code to compare to all other hashes
            k: Desired number of nearest neighbors
            hash_length: Desired to compare the query against

        Returns:

        """
        embed = self.get_embeddings(hash_length)
        orig_vocabulary = np.dot(query, embed)
        ind_sort = np.argsort(-orig_vocabulary)
        return self.tokenizer.ids2tokens(ind_sort[:k])

    @cached(cache=LRUCache(maxsize=8))
    def get_embeddings(self, hash_length: int):
        """Convert all the synapse weights into context independent embeddings. Useful for finding nearest neighbors
        
        Args:
            hash_length: Length of desired hash code

        """
        targets = self.synapses[:, self.n_vocab :]
        act_sort = -np.sort(-targets, axis=0)
        thr = (act_sort[hash_length - 1, :] + act_sort[hash_length, :]) / 2.0
        binary = (targets > thr).astype(np.int8)
        return binary


@cached(cache={})
def get_project(fname):
    return Biohasher(fname)