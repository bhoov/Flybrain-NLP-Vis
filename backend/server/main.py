import argparse
from typing import *
import numpy as np

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import server.api as api
import path_fixes as pf
from biohasher import get_project, softmax

from cachetools import cached

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

@app.get("/api/sentence-to-keywords")
async def sentence_to_keywords(sentence: str):
    project = get_project(pf.PROJECT)
    ids = project.tokenizer.encode(sentence)
    print("IDS: ", ids)
    good_tokens = [project.tokenizer.id2token(id) for id in ids if id not in project.stop_words]
    return good_tokens

@app.get("/api/sentence-to-tokens")
async def sentence_to_tokens(sentence: str):
    project = get_project(pf.PROJECT)
    tokens = project.tokenizer.tokenize(sentence)
    return tokens

@app.get("/api/memory-concepts")
async def get_memory_concepts(head_index: int, n_show:int=20, beta:float=800):
    """Fetch the target concepts for a particular memory"""
    project = get_project(pf.PROJECT)
    return project.get_mem_concepts(head_index, n_show=n_show, beta=beta)

@app.get("/api/n-heads")
async def get_n_heads():
    return get_project(pf.PROJECT).n_heads

@app.get("/api/mem-order")
async def get_mem_order():
    """Get index ordering of heads"""
    project = get_project(pf.PROJECT)
    return [int(m) for m in project.memory_grid]

@app.get("/api/query-top-mems-by-phrase")
async def query_top_mems_by_phrase(phrase: str, beta:float=10.0):

    project = get_project(pf.PROJECT)
    ids = project.tokenizer.encode(phrase)
    v = project.make_sentence_vector(ids)
    activations = softmax(project.synapses @ v, beta)
    ordered_mems = np.argsort(-activations)

    return {
        "activations": [float(a) for a in activations],
        "ordered_heads": [int(m) for m in ordered_mems],
        "head_info": [{"head": int(m), "activation": float(activations[m])} for m in ordered_mems],
        "tokenized_phrase": project.tokenizer.decode(ids)
    }

if __name__ == "__main__":
    # This file is not run as __main__ in the uvicorn environment
    args, _ = parser.parse_known_args()
    uvicorn.run("server:app", host='127.0.0.1', port=args.port)
