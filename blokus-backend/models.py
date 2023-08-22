from pydantic import BaseModel
from typing import Set, Tuple
from uuid import UUID

class Coordinate(BaseModel):
    def __hash__(self):
        return hash((self.x, self.y))

    x: int
    y: int

class Piece(BaseModel):
    shape: Set[Coordinate]

class GameProfile(BaseModel):
    game_id: UUID

class PlayerProfile(BaseModel):
    player_id: int
    color: int
    name: str
