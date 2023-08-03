from pydantic import BaseModel
from typing import Set, Tuple

class Piece(BaseModel):
    shape: Set[Tuple[int,int]]