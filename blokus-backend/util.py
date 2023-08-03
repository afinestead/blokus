from typing import Set

import matplotlib.pyplot as plt

from piece import Piece

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

def generate_pieces(degree) -> Set[Piece]:
    pieces: Set[Piece] = {Piece({(0,0)})}
    new_pieces = None
    for deg in range(1,degree):
        print(f"Generating {deg+1} blokus")
        new_pieces: Set[Piece] = _generate(new_pieces or pieces)
        pieces |= new_pieces
        print(f"{len(new_pieces)} blocks generated, {len(pieces)} blocks total")
    return pieces

def show_piece(piece):
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
    #     show_piece(piece)

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

    total_blocks = 0
    for piece in pieces:
        total_blocks += len(piece)
    print(total_blocks)

    for piece in pieces:
        print(piece)
        show_piece(piece)

    
