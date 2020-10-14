from pathlib import Path
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.models.phrases import Phrases, Phraser
import os
import regex as re
import string
import numpy as np
from typing import *

spattern = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
num_patterns = re.compile(r"(?<=\s|^)(-?[0-9]+\.?[0-9]*)")

PATCH_DICT = {
    "<UNK>": 0,
    "<NUM>": 1,
}

def is_good_line(line):
    """Check if the line is valid"""
    return (len(line) > 1) and ("\x00" not in line)

def line2sentences(line):
    """Convert a line into sentences"""
    line = line.replace('\n', ' ').strip(' ').lower()
    return spattern.split(line)

def replace_nums(line, replace_tok="<NUM>"):
    """Replace all numbers in the line with the special token"""
    return num_patterns.sub(replace_tok, line)

def strip_punc_unicode(line):
    """Strip all punctuation and unicode from the line"""
    line = line.translate(str.maketrans('', '', string.punctuation))
    line = ''.join([c for c in line if c.isascii()])
    return line

def isnum(token):
    return any(t.isdigit() for t in token)

def process_line(line):
    """Compose all transformations to process a line that are desired"""
    sents = line2sentences(line)
    out = []
    for s in sents:
        x = strip_punc_unicode(s)
        xs = x.split()
        xs = [x_ if not isnum(x_) else "<NUM>" for x_ in xs]
        out.append(xs)

    return out

def file2tokens(fname):
    """Convert a file of text into tokenized sentences"""
    with open(fname, 'r', encoding='utf8') as fp:
        chunk = fp.readlines()
        tokenized = []
        for line in chunk:
            if is_good_line(line):
                tokenized += process_line(line)
        return tokenized

class GensimTokenizer:
    def __init__(self, dictionary, phraser=None, patch_dict=PATCH_DICT):
        """Wrap a Gensim Dictionary, phrase detector, and special tokens for creating tokenization from OWT"""
        self.dictionary = dictionary

        if phraser is None:
            self.phraser = Phrases([[]])
        else:
            self.phraser = phraser

        self.patch_dict = patch_dict

    @classmethod
    def from_file(cls, dict_fname, phraser_fname=None):
        d = Dictionary.load(str(dict_fname))
        if phraser_fname is not None:
            p = Phraser.load(phraser_fname)
        else:
            print("WARNING: No phraser specified")
            p = Phraser(Phrases([[]]))
            
        return cls(d, p)

    def add_document_from_fname(self, fname):
        print(f"Adding {fname}")
        tokens = self.phraser[file2tokens(fname)]
        self.dictionary.add_documents(tokens)

    def add_to_phraser_from_fname(self, fname):
        """Detect common phrases from fname for bigramming purposes"""
        print(f"Adding {fname} to phraser")
        tokens = file2tokens(fname)
        self.phraser.add_vocab(tokens)

    def get_dictionary(self):
        return self.dictionary

    def token2id(self, word):
        """Convert a token into an id, converting to UNK as necessary"""
        d = self.dictionary
        return d.token2id.get(word, d.token2id["<UNK>"])

    def tokens2ids(self, tokens):
        """Convert a list of tokens into a ids, converting to UNK as necessary"""
        return [self.token2id(tok) for tok in tokens]

    def tokenize(self, s:str):
        """Convert a sentence into its tokens"""
        return self.phraser[process_line(s)[0]]

    def tokenize_batch(self, lines:List[str]):
        """Convert a batch of lines into their tokens"""
        return self.phraser[[process_line(line)[0] for line in lines]]

    def encode(self, s):
        """Encode a single sentence into IDs"""
        sent_tokens = self.tokenize(s)
        return self.tokens2ids(sent_tokens)

    def decode(self, ids):
        """Alias for `ids2tokens`"""
        return self.ids2tokens(ids)

    def id2token(self, id):
        d = self.dictionary
        if id == -1: return "<STOPWRD>" # Account for post processing
        return d[id] # Add error handling if bad id

    def ids2tokens(self, ids):
        """Convert iterable of ids to tokens"""
        return [self.id2token(id) for id in ids]

    def set_outdir(self, outdir):
        self.outdir = Path(outdir)

    def patch(self, vocab_size, new_vocab, no_below=15, no_above=0.8):
        """Patch the tokenizer with a manually specified list of tokens, after training"""
        
        print("Patching with special tokens...")
        self.dictionary.patch_with_special_tokens(self.patch_dict)
        print("Filtering vocabulary...")
        self.dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=vocab_size)

        print(f"Adding {len(new_vocab)} new words to dictionary...")
        new_vocab = self.tokenize_batch(new_vocab)
        self.dictionary.add_documents(new_vocab)
        print(f"Done patching. New vocab size = {self.n_vocab()}")
        return new_vocab

    def save(self, outfile):
        self.dictionary.save(outfile)

    def n_vocab(self):
        return len(self.dictionary.keys())

    def __len__(self):
        return len(self.dictionary.keys())

    def encode_sentences_from_fname(self, fname):
        outlist = []
        ind_offsets = []
        new_start = 0

        with open(fname, 'r') as fp:
            for line in fp.readlines():
                if is_good_line(line):
                    sents = self.phraser[process_line(line)]
                    for sent in sents:
                        ids = self.tokens2ids(sent)
                        outlist += ids
                        new_start = new_start + len(ids)
                        ind_offsets.append(new_start)

        return np.asarray(outlist, dtype=np.int32), np.asarray(ind_offsets, dtype=np.uint64)

    def encode_and_save_for_mp(self, fname):
        """Save sentences from fname. Needed because a local function can't be used with the MP module"""
        if self.outdir is None: raise ValueError("Please `set_outdir` first")

        fname = Path(fname)

        idarr_outfile = self.outdir / (fname.stem + '.npy')
        ind_offsets_outfile = self.outdir / (fname.stem + '_offsets.npy')
        idarr, ind_offsets = self.encode_sentences_from_fname(fname)
        np.save(idarr_outfile, idarr)
        np.save(ind_offsets_outfile, ind_offsets)
