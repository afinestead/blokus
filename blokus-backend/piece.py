import numpy as np

from typing import Set, Tuple


class Piece:
    def __init__(self, squares: Set[Tuple] = set()):
        sqs = set()
        for sq in squares:
            sqs.add(sq) 
        self.squares: Set[Tuple] = set(sorted(sqs))
    
    def __eq__(self, other):
        return self.squares == other.squares
    
    def __hash__(self):
        return hash(tuple(self.squares))
    
    def __len__(self):
        return len(self.squares)
    
    def __copy__(self):
        return Piece(self.squares.copy())
    
    def __add__(self, square: Tuple):
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
        def rot(pt):
            return (pt[0]*cos - pt[1]*sin, pt[1]*cos + pt[0]*sin)
        return Piece(rot(block) for block in self)

    def reflect(self, x_ax=True):
        def ref(pt):
            return (pt[0], -pt[1]) if x_ax else (-pt[0], pt[1])
        return Piece(ref(block) for block in self)
    
    def translate(self):
        min_x = min(block[0] for block in self)
        min_y = min(block[1] for block in self)
        return Piece((x - min_x, y - min_y) for x,y in self)