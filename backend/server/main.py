import argparse
from typing import *
import numpy as np
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import server.api as api
import server.path_fixes as pf
from server.utils import round_2d_nested_list, round_1d_list
from biohasher import get_project
from indexer import BiohashIndexer

from cachetools import cached

@cached(cache={})
def get_indexer(h5_fname=pf.H5_CORPUS, enc_file=pf.ENCS, off_file=pf.OFFS):
    return BiohashIndexer(h5_fname, enc_file, off_file)

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--port", default=8000, type=int, help="Port to run the app. ")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main routes
@app.get("/")
def index(): return RedirectResponse(url="client/index.html")

# the `file_path:path` says to accept any path as a string here. Otherwise, `file_paths` containing `/` will not be served properly
@app.get("/client/{file_path:path}")
def send_static_client(file_path:str):
    """ Serves (makes accessible) all files from ./client/ to ``/client/{path}``

    Args:
        path: Name of file in the client directory
    """
    f = str(pf.DIST / file_path)
    print("Finding file: ", f)
    return FileResponse(f)

# ======================================================================
## MAIN API ##
# ======================================================================

@app.get("/api/sentence-to-tokens")
async def sentence_to_tokens(sentence: str):
    project = get_project(pf.PROJECT)
    tokens = project.tokenizer.tokenize(sentence)
    return tokens

@app.post("/api/attentions-from-tokens")
async def attentions_from_tokens(payload: api.AttentionFromTokenPayload):
    tokens = payload['tokens']
    target_idx = payload['target_idx']
    hash_length = payload['hash_length']

    project = get_project(pf.PROJECT)
    token_ids = project.tokenizer.tokens2ids(tokens)
    output = project.get_hash_from_token_ids(token_ids, target_idx, hash_length)

    return {
        "tokens": tokens,
        "token_ids": token_ids,
        "target_idx": target_idx,
        "context_attentions": round_2d_nested_list(output['context_attentions'].tolist(), 6),
        "target_attentions": round_1d_list(output['target_attentions'].tolist(), 6) if target_idx is not None else None,
        "activated_neurons": output['activated_neurons'].tolist(),
        "hashcode": output['hash'].tolist()
    }

@app.post("/api/get-k-nearest-context-independent")
async def get_k_nearest_context_independent(payload: api.KNearestPayload):
    hash_query = payload["hash_query"]
    k = payload["k"]
    hash_length = payload["hash_length"]

    project = get_project(pf.PROJECT)
    k_nearest_tokens = project.get_k_neighbors(hash_query, k, hash_length)

    return {
        "tokens": k_nearest_tokens,
    }

@app.post("/api/get-k-nearest-context-dependent")
async def get_k_nearest_context_dependent(payload: api.KNearestPayload):
    hash_query = payload["hash_query"]
    k = payload["k"]
    hash_length = payload["hash_length"]

    indexer = get_indexer()

    project = get_project(pf.PROJECT)

    start = datetime.now()
    res = indexer.get_k_nearest(np.array(hash_query), k)
    print(f"Indexing took {datetime.now() - start} seconds")

    def parse_nearest(sim, toks, wgram_ind, target_ind, wgram):
        return {
            "sentence_tokens": project.tokenizer.ids2tokens(toks),
            "sim_score": sim,
            "wgram_start": wgram_ind,
            "wgram": project.tokenizer.ids2tokens(wgram),
            "target_start": target_ind,
        }

    json_output = [parse_nearest(sim, toks, wg, ti, gram) for sim, toks, wg, ti, gram in zip(res['sims'], res['sentence_tokens'], res['wgram_inds'], res['target_inds'], res['wgrams'])]
    return json_output

if __name__ == "__main__":
    # This file is not run as __main__ in the uvicorn environment
    args, _ = parser.parse_known_args()
    uvicorn.run("server:app", host='127.0.0.1', port=args.port)
