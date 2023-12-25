from typing import List, Set

# import matplotlib.pyplot as plt

import models
from board import Board
from piece import Piece


def find_in_set(piece: Piece, unique: Set[Piece]):
    for rot in (0, 90, 180, 270):
        rotated = piece.rotate(rot).translate()
        reflected = rotated.reflect().translate()
        if rotated in unique:
            return rotated
        if reflected in unique:
            return reflected
    return None

def _generate(pieces: Set[Piece]) -> Set[Piece]:
    gen_up  = lambda p: models.Coordinate(x=p.x-1,y=p.y)
    gen_down = lambda p: models.Coordinate(x=p.x+1,y=p.y)
    gen_left  = lambda p: models.Coordinate(x=p.x,y=p.y-1)
    gen_right    = lambda p: models.Coordinate(x=p.x,y=p.y+1)

    new_pieces: Set[Piece] = set()

    for piece in pieces:
        for block in piece:
            for neighbor_gen in (gen_left, gen_right, gen_down, gen_up):
                neighbor = neighbor_gen(block)
                print(neighbor)
                new_piece = (piece + neighbor).translate()
                print(new_piece)
                if find_in_set(new_piece, new_pieces) is None:
                    new_pieces.add(new_piece)
    return new_pieces

def generate_pieces(degree) -> Set[Piece]:
    pieces: Set[Piece] = {Piece({models.Coordinate(x=0,y=0)})}
    new_pieces = None
    for deg in range(1,degree):
        print(f"Generating {deg+1} blokus")
        new_pieces: Set[Piece] = _generate(new_pieces or pieces)
        pieces |= new_pieces
        print(f"{len(new_pieces)} blocks generated, {len(pieces)} blocks total")
    return pieces


def open_corners(board: Board, pid: int) -> List[models.Coordinate]:
    for i, row in enumerate(board.board):
        for j, owner in enumerate(row):
            if owner is None:
                coord = models.Coordinate(x=i, y=j)
                if (i,j) == (0,0) and not board.occupied_by_player(pid, coord):
                    yield coord
                if board.has_valid_corner(coord, pid):
                    yield coord

def has_legal_move(board: Board, pid: int, pieces: Set[Piece]):
    return True
    for corner in open_corners(board, pid):
        for piece in pieces:
            for rotation in (0, 90, 180, 270):
                rotated = piece.rotate(rotation)
                if board.valid_placement(rotated.translate(), corner, pid):
                    return True
                reflected = rotated.reflect()
                if board.valid_placement(reflected.translate(), corner, pid):
                    return True
            
    
    return False


def generate_board(n_players, piece_degree):
    '''
    [####, ####] 2
    [####, ####] 2

    [None, ####, ####, None]  2
    [####, ####, ####, ####]  4
    [####, ####, ####, ####]  4
    [None, ####, ####, None]  2
    
    [None, None, None, ####, ####, None, None, None]  2
    [None, None, None, ####, ####, None, None, None]  2
    [None, None, ####, ####, ####, ####, None, None]  4
    [None, None, ####, ####, ####, ####, None, None]  4
    [####, ####, ####, ####, ####, ####, ####, ####]  8
    [####, ####, ####, ####, ####, ####, ####, ####]  8
    [None, None, ####, ####, ####, ####, None, None]  4
    [None, None, ####, ####, ####, ####, None, None]  4
    [None, None, None, ####, ####, None, None, None]  2
    [None, None, None, ####, ####, None, None, None]  2
    
    '''
    lateral_len = piece_degree * 4

    def middle_n_idx(n, len):
        # n = 1, len = 1, -> [0]
        # n = 1, len = 3, -> [1]
        # n = 1, len = 5, -> [2]
        # n = 3, len = 3, -> [0,1,2]
        # n = 3, len = 5, -> [1,2,3]
        pass


    board_deg = (((n_players - 1) // 4) * 2) + 1
    print(board_deg)
    for cols in range(0, board_deg, 2):
        cols = cols + 1
        print(cols)
        row = [None]*board_deg
        row[(cols//2)-cols:cols] = "X"
        row[cols//2 - cols:cols//2] = "X"
        print(row)


    # max_lateral_len = lateral_len * board_deg

    # row_duplicates = 2

    # board = []

    # print(lateral_len, board_deg)

    # for row in range(board_deg):
    #     r = [None]*lateral_len*(row+1)
    #     board.append()

    # for row in range(board_deg, 0, -1):
    #     print(row)
    #     board.append([None]*lateral_len*(row))
    
    # return board
    






def show_piece(piece):
    # fig = plt.figure()
    # plt.xlim(0, degree)
    # plt.ylim(0, degree)
    # for block in piece:
    #     plt.gca().add_patch(plt.Rectangle(block, 1, 1, fc="blue", ec="black"))

    # plt.show()
    pass

if __name__ == "__main__":
    # print(generate_board(4, 5))

    print(generate_pieces(2))

    # pid = 1
    # p1 = Piece({(0,0)})
    # p2 = Piece({(0,0), (1,0)})

    # b = Board(4)
    # b.place(p1, models.Coordinate(x=0,y=0), pid)
    # print(b)
    # for corner in open_corners(b, pid):
    #     print(corner)

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

    # degree = 12
    # pieces = generate_pieces(degree)
    # print(len(pieces))

    # total_blocks = 0
    # for piece in pieces:
    #     total_blocks += len(piece)
    # print(total_blocks)

    # for piece in pieces:
    #     print(piece)
    #     show_piece(piece)

    
