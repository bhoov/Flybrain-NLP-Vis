import numpy as np
import h5py
from typing import *
from pathlib import Path
from cachetools import cached
from datetime import datetime

def make_hash_matrix(argsorts, hash_length):
    """Convert a dataset of hash lengths from argsorted activations"""
    codes = np.zeros_like(argsorts, dtype=np.int8)
    for i in range(codes.shape[0]):
        codes[i][argsorts[i][:hash_length]] = 1
        
    return codes

class BiohashIndexer:
    def __init__(self, h5_file:Union[str, Path], enc_npy_file:Union[str, Path], offs_npy_file:Union[str, Path]):
        self.h5_file = Path(h5_file)
        self.f = h5py.File(str(self.h5_file), 'r') 
        self.activations = self.f['activations']
        self.encodings = np.load(enc_npy_file, mmap_mode="r")
        self.offsets = np.load(offs_npy_file, mmap_mode="r")
        self.sentence_ids = self.f['sentence_ids']
        self.weights = self.f['weights']
        self.W = self.f.attrs['W']
        self.k = self.f.attrs['k']
        self.N, self.h = self.activations.shape
        self.target_offset = int(self.W / 2)

        self._sorted_activation_idxs = None
        self._wgrams = None 
        
    @property
    def sorted_activation_idxs(self):
        """Activations argsorted from 0 (highest) to h (lowest)"""
        if self._sorted_activation_idxs is None:
            self._sorted_activation_idxs = np.array(self.f['codes'])
        return self._sorted_activation_idxs

    @property
    def wgrams(self):
        if self._wgrams is None:
#             self._wgrams = np.array(self.f['wgrams'])
            self._wgrams = self.f['wgrams']
        return self._wgrams

    def max_sims_inds(self, query:np.ndarray, k:int):
        """Return k indices of the most similar arrays"""
        hash_length = int(query.sum())
        hash_codes = make_hash_matrix(self.sorted_activation_idxs, hash_length)
        sims = hash_codes @ query
        inds = np.argsort(-sims)[:k]
        return sims, inds

    def get(self, idx:int):
        """Get the information for the W-Gram idx `idx` in the corpus"""
        act = self.activations[idx]
        code = self.sorted_activation_idxs[idx]
        sid = self.sentence_ids[idx]

        wgram_start = self.wgrams[idx]
        wgram = self.encodings[int(wgram_start):int(wgram_start + self.W)]

        return {
            "activations": act, # Raw activations
            "code": code, # Argsorted activations
            "wgram": wgram, # Wgram
            "sentence_id": sid,
        }

    def sentence_from_sid(self, sid:int):
        """Return the sentence associated with a sentence id"""
        return self.encodings[int(self.offsets[sid]):int(self.offsets[int(sid+1)])]

    def get_k_nearest(self, query:np.ndarray, k:int):
        sims, inds = self.max_sims_inds(query, k)

        # ind_order = np.argsort(inds)

        # h5py can only work on indexes increasing. This fixes that
        # def index_hdf5(arr, inds, idx_order=None):
        #     if idx_order is None: idx_order = np.argsort(inds)
        #     return arr[inds[ind_order]][::-1][ind_order][::-1]

        # wgrams = index_hdf5(self.wgrams, inds, ind_order)
        # s_ids = index_hdf5(self.sentence_ids, inds, ind_order)

        s_ids = [self.sentence_ids[i] for i in inds]
        wgrams = [self.wgrams[i] for i in inds]
        offsets = [self.offsets[s] for s in s_ids]
        wgrams_offset = np.array(wgrams) - np.array(offsets)

        out = {
            "sims": sims[inds].tolist(),
            "sentence_tokens": [self.sentence_from_sid(i).tolist() for i in s_ids],
            "wgram_inds": wgrams_offset.tolist(), # Relative to start of that sentence's tokens
            "wgrams": [self.encodings[wgram:int(wgram + self.W)] for wgram in wgrams],# Tokens of the matched wgram
            "target_inds": (wgrams_offset + self.target_offset).tolist(), # Relative to start of that sentence's tokens
            "W": self.W,
        }

        return out