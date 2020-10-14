from pathlib import Path
import os

# SERVING STATIC FILES
ROOT = Path(
    os.path.abspath(__file__)
).parent.parent.parent  # Root directory of the project
SRC = ROOT / "src"
CLIENT = ROOT / "client"
PUBLIC = CLIENT / "public"
DIST = PUBLIC
DATA = ROOT / "data"

PROJECT = ROOT / "biohash_project.yaml"
REF = DATA / "annotations"
# H5_CORPUS = REF / "leo_correlations_100k_codes_uint16.hdf5"
H5_CORPUS = REF / "leo_info_coef_50k_50t.hdf5"
ENCS = REF / "encodings.npy"
OFFS = REF / "offsets_0.npy"