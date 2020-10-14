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
from biohasher import get_project

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

@app.get("/api/sentence-to-tokens")
async def sentence_to_tokens(sentence: str):
    project = get_project(pf.PROJECT)
    tokens = project.tokenizer.tokenize(sentence)
    return tokens

@app.get("/api/get-memory-concepts")
def get_memory_concepts(head_index: int, n_show:int=20, beta:float=800):
    """Fetch the target concepts for a particular memory"""
    project = get_project(pf.PROJECT)
    return project.get_mem_concepts(head_index, n_show=n_show, beta=beta)

if __name__ == "__main__":
    # This file is not run as __main__ in the uvicorn environment
    args, _ = parser.parse_known_args()
    uvicorn.run("server:app", host='127.0.0.1', port=args.port)
