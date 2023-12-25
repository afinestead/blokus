import numpy as np

from typing import Set

from models import Coordinate

class Piece:
    def __init__(self, squares: Set[Coordinate] = set()):
        sqs = set()
        for sq in squares:
            sqs.add(sq) 
        self.squares: Set[Coordinate] = set(sorted(sqs))
    
    def __eq__(self, other):
        return self.squares == other.squares
    
    def __hash__(self):
        return hash(tuple(self.squares))
    
    def __len__(self):
        return len(self.squares)
    
    def __copy__(self):
        return Piece(self.squares.copy())
    
    def __add__(self, square: Coordinate):
        sqs = self.squares.copy()
        sqs.add(square)
        return Piece(sqs)
    
    def __iter__(self):
        return self.squares.__iter__()
    
    def __str__(self):
        return str(self.squares)
    
    def rotate(self, deg):
        as_rad = np.deg2rad(deg)
        cos = int(np.cos(as_rad))
        sin = int(np.sin(as_rad))
        def rot(pt) -> Coordinate:
            return Coordinate(x=pt.x*cos - pt.y*sin, y=pt.y*cos + pt.x*sin)
        return Piece(rot(block) for block in self)

    def reflect(self, x_ax=True):
        def ref(pt) -> Coordinate:
            return Coordinate(x=pt.x, y=-pt.y) if x_ax else Coordinate(x=-pt.x, y=pt.y)
        return Piece(ref(block) for block in self)
    
    def translate(self):
        min_x = min(block.x for block in self)
        min_y = min(block.y for block in self)
        return Piece(Coordinate(x=block.x-min_x, y=block.y-min_y) for block in self)