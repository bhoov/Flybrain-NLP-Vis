""" Helper functions for tokenizing OpenWebText in parallel """
import os
import ray
import psutil
from pathlib import Path
import numpy as np
import multiprocessing
import time
from gensim.corpora import Dictionary
from gensim.models.phrases import Phrases, Phraser
from tokenizer import GensimTokenizer, PATCH_DICT
import path_fixes as pf

num_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_cpus)

@ray.remote
class StreamingDictionary:
    def __init__(self, phraser=None, prune_at=50000):
        self.tokenizer = GensimTokenizer(Dictionary(prune_at=prune_at), phraser)

    def add_document_from_fname(self, fname, i=None):
        if i is not None:
            if (i+1) % 100 == 0:
                print(f"Starting {i}")
        self.tokenizer.add_document_from_fname(fname)

    def get_dictionary(self):
        return self.tokenizer.dictionary

def make_tokenizer(data_dir, out_fname, phraser_fname=None, glob_pattern="*_data"):
    data_dir = Path(data_dir)
    out_fname = Path(out_fname)
    outdir = out_fname.parent
    if not outdir.exists(): outdir.mkdir(parents=True)

    fnames = list(data_dir.glob("*_data"))
    if phraser_fname is not None:
        p = Phraser.load(phraser_fname) 
    else:
        p = Phraser([[]])
    actors = [StreamingDictionary.remote(p) for _ in range(num_cpus)]

    for i, f in enumerate(data_dir.glob("*_data")):
        actors[i % num_cpus].add_document_from_fname.remote(f, i)

    # Aggregate all of the results.
    print("\n\n\nAggregating the results. Could take a while:\n")
    dictionaries = ray.get([actor.get_dictionary.remote() for actor in actors])
    d = Dictionary()
    for d_ in dictionaries:
        d.merge_with(d_)

    # Save raw dictionary
    d.save(str(out_fname))

def make_phraser(data_dir, out_fname, min_count=8, threshold=10, scorer="npmi", stop_word_file=None, glob_pattern="*_data"):
    data_dir = Path(data_dir)
    out_fname = Path(out_fname)
    outdir = out_fname.parent
    if not outdir.exists(): outdir.mkdir(parents=True)

    if stop_word_file is not None:
        with open(stop_word_file, 'r') as fp:
            stop_words = [line.strip() for line in fp]
    else:
        stop_words = []

    fnames = list(data_dir.glob("*_data"))

    common_terms = frozenset(list(PATCH_DICT.keys()) + stop_words)
    tokenizer = GensimTokenizer(Dictionary(prune_at=50000), Phrases([[]], min_count=min_count, threshold=threshold, scoring=scorer, max_vocab_size=50000, common_terms=common_terms))
    # tokenizer = GensimTokenizer(Dictionary(prune_at=50000), Phrases([[]], scoring=scorer, max_vocab_size=50000, common_terms=stop_words))

    for i, f in enumerate(data_dir.glob("*_data")):
        if (i % 10) == 0: print(f"Starting document {i}")
        tokenizer.add_to_phraser_from_fname(f)

    print("Saving phraser...")
    tokenizer.phraser.save(str(out_fname))

def patch_tokenizer(infile, outfile, phraser_file, vocab_size=20000, added_vocab_file=None, no_above=0.8, no_below=15):
    infile = Path(infile)
    outfile = Path(outfile)
    if not outfile.parent.exists(): outfile.parent.mkdir(parents=True)

    print("Loading dictionary (takes a bit)...")
    tokenizer = GensimTokenizer.from_file(str(infile), str(phraser_file))

    if added_vocab_file is not None:
        print("Adding content from additional file")
        with open(added_vocab_file, 'r') as fp:
            new_vocab = [line.strip().lower() for line in fp]
    else:
        new_vocab = []

    tokenizer.patch(vocab_size, new_vocab, no_below=no_below, no_above=no_above)

    tokenizer.save(str(outfile))

    print(f"Saved to {outfile}")


def encode(datadir, outdir, model, phraser, glob="*_data"):
    datadir = Path(datadir)
    outdir = Path(outdir)
    if not outdir.exists(): outdir.mkdir(parents=True)

    tok = GensimTokenizer.from_file(model, phraser)
    tok.set_outdir(outdir)

    starttime = time.time()

    fnames = datadir.glob(glob)

    print("Starting multiprocessing")
    pool = mp.Pool()
    pool.map(tok.encode_and_save_for_mp, fnames)
    pool.close()
    pool.join()
    print('That took {} seconds'.format(time.time() - starttime))

def from_npyfile(fname):
    return np.load(str(fname), mmap_mode=None)

def combine_npyfiles(fnames, outfname, inc_offset=False):
    starttime = time.time()

    print("Getting arrays from files into memory")

    arrays = list(map(from_npyfile, fnames))
    N = len(arrays)

    if inc_offset:
        offset_sent_by = [v[-1] for i, v in enumerate(arrays)]
        for i in range(len(arrays)):
            offset = sum(offset_sent_by[:i])
            arrays[i] = arrays[i] + sum(offset_sent_by[:i])

    print("Starting concatenation...")
    array_lens = [len(a) for a in arrays]
    total_len = sum(array_lens)

    if inc_offset:
        dtype = np.uint64
    else:
        dtype = np.int32

    tmpfname = Path(Path(outfname).stem + '.tmp')
    out = np.memmap(tmpfname, dtype=dtype, mode='w+', shape=(total_len,))

    starti = 0
    for i, length in enumerate(array_lens):
        stopi = starti+length
        out[starti:stopi] = arrays[i]
        if (i % 100) == 0:
            print("Finished ", i, " out of ", N)
        starti = stopi

    print(f"Finished processing for {outfname}. Saving array of shape {out.shape}. Took {time.time() - starttime} seconds")

    if inc_offset:
        print("Concatenating offsets...")
        out = np.hstack([np.array(0, dtype=dtype), out[:-1]])

    np.save(outfname, out, allow_pickle=False)
    del out
    tmpfname.unlink()

def combine_all(split_encoding_dir, out_dir):
    split_encoding_dir = Path(split_encoding_dir)
    out_dir = Path(out_dir)
    if not out_dir.exists(): out_dir.mkdir(parents=True)

    npfs = list(split_encoding_dir.glob("*.npy"))
    offset_fs = [f for f in npfs if 'offset' in str(f)]
    id_fs = [f for f in npfs if 'offset' not in str(f)]

    offset_fs.sort()
    id_fs.sort()

    enc_fname_out = out_dir / "encodings.npy"
    offset_fname_out = out_dir / "offsets.npy"

    combine_npyfiles(id_fs, enc_fname_out)
    combine_npyfiles(offset_fs, offset_fname_out, inc_offset=True)

    print("Finished!")
