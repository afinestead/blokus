from copy import copy, deepcopy

from typing import List, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np


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

def is_unique(piece: Piece, unique: Set[Piece]):
    for rot in (0, 90, 180, 270):
        rotated = piece.rotate(rot)
        reflected = rotated.reflect()
        if rotated.translate() in unique or reflected.translate() in unique:
            return False
    return True

def _generate(pieces: Set[Piece]) -> Set[Piece]:
    gen_left  = lambda p: (p[0]-1,p[1])
    gen_right = lambda p: (p[0]+1,p[1])
    gen_down  = lambda p: (p[0],p[1]-1)
    gen_up    = lambda p: (p[0],p[1]+1)

    new_pieces: Set[Piece] = set()

    for piece in pieces:
        for block in piece:
            for neighbor_gen in (gen_left, gen_right, gen_down, gen_up):
                neighbor = neighbor_gen(block)
                new_piece = (piece + neighbor).translate()
                if is_unique(new_piece, new_pieces):
                    new_pieces.add(new_piece)
    return new_pieces

def generate_pieces(degree):
    pieces: Set[Piece] = {Piece({(0,0)})}
    new_pieces = None
    for deg in range(1,degree):
        print(f"Generating {deg+1} blokus")
        new_pieces: Set[Piece] = _generate(new_pieces or pieces)
        pieces |= new_pieces
        print(f"{len(new_pieces)} blocks generated, {len(pieces)} blocks total")
    return pieces

def print_piece(piece):
    fig = plt.figure()
    plt.xlim(0, degree)
    plt.ylim(0, degree)
    for block in piece:
        plt.gca().add_patch(plt.Rectangle(block, 1, 1, fc="blue", ec="black"))

    plt.show()

if __name__ == "__main__":
    # pieces = generate_pieces(degree)
    # print(pieces)
    # print(len(pieces))
    # for piece in pieces:
    #     print_piece(piece)

    # p1 = Piece({(0,0), (0,1), (1,0)})
    # p2 = Piece({(0,0), (1,0), (0,1)})
    # p3 = Piece({(0,2), (0,1), (0,0), (1,0), (2,0)})

    # print(p1, p2)
    # assert(p1 == p2)

    # for p in p1:
    #     print(p)

    # for deg in (0,90,180,270):
    #     print(p1.rotate(deg))
    
    # print(p1, p1.reflect().translate())

    # assert(not is_unique(p1, {p2}))
    # assert(is_unique(p1, {p3}))

    degree = 12
    pieces = generate_pieces(degree)
    print(len(pieces))
    for piece in pieces:
        print(piece)
        print_piece(piece)

    # num_pieces = len(pieces)

    # rows = int(np.floor(np.sqrt(num_pieces)))
    # cols = int(np.ceil(num_pieces/rows))
    # fig, axs = plt.subplots(rows, cols)
    
    
    # for i, piece in enumerate(pieces):
    #     r = i // cols
    #     c = i // rows
    #     print(r,c)
    #     ax = axs[r,c]
    #     print_piece(ax, piece)
    # plt.show()
        # print(piece)
        # print_piece(piece)
    
