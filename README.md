# Flybrain-Vis

Visualize the Associative memory trained in a biologically plausible way on word embeddings

### Setting up the Environment

```bash
conda env create -f environment.yml; \
conda env create -f environment-dev.yml; \ # optional
conda activate flybrain; \
pip install -e .
```

### Getting data

The model requires 3 primary files:
1. Synapse weights
2. Tokenizer file
3. Stop words used in the tokenization

The paths to these are defined in a `biohash_project.yaml`

Luckily, these files have been uploaded to a bucket on the cloud using `dvc`, installed in the conda environment.

**STEPS**
1. Contact Ben for the `.dvc/config` file (should not be published to git). 
2. `dvc pull`

### Starting the Server

`uvicorn backend.server:app --reload`

### Running the Client 

(development)
`cd client; npm run dev`