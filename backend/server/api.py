from pydantic import BaseModel
import numpy as np
from typing import *

class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash(self.json())

    @classmethod
    def validate(cls, v: np.ndarray):
        return v

class AttentionFromTokenPayload(HashableBaseModel):
    tokens: List[str]
    target_idx: Optional[int] = None
    hash_length: int = 32

class KNearestPayload(HashableBaseModel):
    hash_query: List[int] # Query hash code
    k: int = 10 # Number of neighbors to return
    hash_length: int = 32 # Length of hash to consider in vocabulary

class GoodbyePayload(HashableBaseModel):
    firstname:str
