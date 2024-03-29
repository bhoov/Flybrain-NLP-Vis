import yaml
import os
import numpy as np
from tokenizer import GensimTokenizer
from pathlib import Path
from functools import cached_property
from cachetools import cached, LRUCache
from typing import *
import project_config as pc

def softmax(x: np.array, beta=1.0):
    """Take the softmax of 1-D vector `x` according to inverse temperature `beta`. Returns a vector of the same length as x"""
    v = np.exp(beta*x)
    return v / np.sum(v)

def normalize_synapses(syn: np.array, prec=1.0e-32, p=2):
    """Normalize the synapses

    Args:
        syn: The matrix of learned synapses
        prec: ??
        p: Of the p-norm

    Returns:
        Normalized array of the given synapses
    """
    K, N = syn.shape
    nc = np.power(np.sum(syn**p,axis=1),1/p).reshape(K,1)
    return syn / np.tile(nc + prec, (1, N))

class Biohasher:
    """A class wrapper around a tokenizer, stop words, and synapse weights for hashing words"""

    def __init__(self, synapse_file: Union[Path, str], tokenizer_file: Union[Path, str], stopword_file: Optional[Union[Path, str]]=None, phrases_file: Optional[Union[Path, str]]=None, normalize_synapses: bool=True):

        self.synapse_file = str(synapse_file)
        self.tokenizer_file = str(tokenizer_file)
        self.stopword_file = str(stopword_file) if stopword_file is not None else None
        self.phrases_file = str(phrases_file) if phrases_file is not None else None
        self.normalize_synapses = normalize_synapses

    @classmethod
    def from_config(cls, fname: Union[Path, str]):
        fpath = Path(fname)
        ref_dir = fpath.parent

        with open(fname, "r") as fp:
            conf = yaml.load(fp, Loader=yaml.FullLoader)

        synapse_file = ref_dir / conf["synapses"]
        tokenizer_file = ref_dir / conf["tokenizer"]
        phrases_file = ref_dir / conf["phrases"] if "phrases" in conf.keys() else None
        stopword_file = ref_dir / conf["stop_words"] if "stop_words" in conf.keys() else None
        normalize_synapses = conf.get("normalize_synapses", False)


        return cls(synapse_file, tokenizer_file, stopword_file=stopword_file, phrases_file=phrases_file, normalize_synapses=normalize_synapses)

    @cached_property
    def n_heads(self):
        H, _ = self.synapses.shape
        return H

    @cached_property
    def synapses(self):
        print("Loading synapses...")
        syn = np.load(self.synapse_file)

        if self.normalize_synapses:
            return normalize_synapses(syn)
        return syn

    @cached_property
    def tokenizer(self):
        print("Loading Tokenizer...")
        return GensimTokenizer.from_file(self.tokenizer_file, self.phrases_file)

    @cached_property
    def stop_words(self):
        """Words that are intentionally not learned by the model"""
        print("Loading stop words...")
        return set(np.load(self.stopword_file))

    @cached_property
    def n_vocab(self):
        return self.tokenizer.n_vocab()

    @cached_property
    def memory_grid(self):
        """Return the indices of all the heads as a grid ordered by a Kohonen map"""
        return np.load(pc.MEM_ORDER)

    def make_sentence_vector(self, token_ids: Iterable[int], targ_idx=None, targ_coef=1, targ_coef_is_n_context=False, normalize_vector=True, return_n_context=False, ignore_unknown=True):
        """Create the input for the synapses given the token ids
        
        Args:
            token_ids: Tokenized input
            targ_idx: Which index to treat as the target index. Must be [0, len(token_ids))
            targ_coef: Force the target index to have this value
            targ_coef_is_n_context: Set target value to number of context. If true, overrides targ_coef.
            normalize_vector: If provided, normalize each element by the total number of tokens
            return_n_context: Get information about the number of context tokens 
            ignore_unknown: If the token is not in the vocabulary, do not add it to the sentence vector as "unknown"

        Returns:
            Sentence vector (np.array of shape (N_vocab,))
        """
        H, N = self.synapses.shape
        sentence = np.zeros((N,), dtype=np.int8)
        vocab = self.tokenizer.dictionary.keys()

        def valid_token(t): 
            is_unknown = ignore_unknown and t != self.tokenizer.patch_dict["<UNK>"]
            return t in vocab and t not in self.stop_words and is_unknown

        # Assign context
        n_context = 0
        for i, t in enumerate(token_ids):
            if i != targ_idx:
                if valid_token(t):
                    n_context += 1
                    sentence[t] += 1

        # Assign target
        if targ_coef_is_n_context: 
            target_value = n_context
        else:
            target_value = targ_coef

        if targ_idx is not None:
            target = token_ids[targ_idx]
            if target not in self.stop_words:
                sentence[self.n_vocab + target] = target_value

        if normalize_vector:
            divisor = np.sqrt(np.sum(sentence * sentence))
            if divisor > 0:
                sentence = sentence / divisor # Could be optimized as vector is very sparse

        if return_n_context:
            out = (sentence, n_context)
        else:
            out = sentence

        return out

    def phrase2sentence_vector(self, phrase: str, normalize_vector=True, ignore_unknown=True):
        """Encode a sentence, then create a context only vector out of a phrase"""
        ids = self.tokenizer.encode(phrase)
        return self.make_sentence_vector(ids, normalize_vector=normalize_vector, ignore_unknown=ignore_unknown)

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

    def get_mem_concepts(self, h: int, n_show: int=20, beta: float=800.0, no_masking=False):
        """Retrieve a ranked list of `n` concepts that head `h` learns, weighting them according to inverse temperature `beta`
        
        Right now, only supports target compartment retrievals

        Args:
            h: Which neuron to inspect
            n_show: How many concepts to retrieve
            beta: Inverse temperature used to calculate contributions
            no_masking: If true, do not hide offensive concepts. 
        """
        # context = softmax(self.synapses[h][:self.n_vocab], beta)
        target = softmax(self.synapses[h][self.n_vocab:], beta)
        output = [
            {
            "token": self.tokenizer.id2token(ID),
            "contribution": float(target[ID])
            } for ID in np.argsort(-target)[:n_show]
        ]

        if no_masking: return output

        # IN PLACE
        label = self.get_label_from_head(h)
        def mask_bad_token_(t, mask="<MASK>"):
            """Modify a token in place if it is bad"""
            for bad_tok in pc.SENSITIVE_CONCEPTS[label]:
                if bad_tok in t['token']:
                    t['token'] = mask

        if label in pc.SENSITIVE_CONCEPTS.keys(): [mask_bad_token_(t) for t in output]

        return output


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

    def get_head_by_labeled_index(self, idx):
        """Convert the displayed label (assigned by memory_grid) into the logical index"""
        return self.memory_grid[idx]

    def get_label_from_head(self, head):
        """Convert the head index to displayed label (assigned by memory_grid)"""
        return np.where(self.memory_grid == head)[0][0]


@cached(cache={})
def get_project(fname):
    return Biohasher.from_config(fname)