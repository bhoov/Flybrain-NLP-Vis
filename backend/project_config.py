from pathlib import Path
import os

# Fixed Paths
ROOT = Path(
    os.path.abspath(__file__)
).parent.parent  # Root directory of the project
SRC = ROOT / "src"
CLIENT = ROOT / "client"
PUBLIC = CLIENT / "public"
DIST = PUBLIC
DATA = ROOT / "data"
MEM_ORDER = DATA / "indices_of_memories.npy"
PROJECT = ROOT / "biohash_project.yaml"

# Sensitive Concepts {neuronLabel: wordPartsToMask[]}
SENSITIVE_CONCEPTS = {
    199: ["black", "matter"],
    249: ["genital"],
    286: ["criminal"],
    399: ["illegally"]
}