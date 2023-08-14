from threading import Lock
from typing import Tuple

from piece import Piece

class Board:
    # only ever one Board object with consistent board state

    def __init__(self, dimension, onupdate):
        self.dimension = dimension
        self.board = [[None]*dimension for _ in range(dimension)]
        self.lock = Lock()
        self.onupdate = onupdate
    
    def __str__(self):
        s = "[" + "---"*self.dimension + "]\n"
        for i, _ in enumerate(self.board):
            s += "["
            for j, _ in enumerate(self.board):
                s += "   " if not self.board[i][j] else f" {self.board[i][j]} "
            s += "]\n"
        s += "[" + "---"*self.dimension + "]"
        return s

    def __enter__(self):
        try:
            with self.lock:
                return self
        except:
            pass
    
    def __exit__(self, *_exc):
        pass
    
    async def place(self, piece: Piece, origin: Tuple, player: int):
        x,y = origin
        for xp,yp in piece:
            square = self.board[y+yp][x+xp]
            assert(square is None)
            self.board[y+yp][x+xp] = player
            await self.onupdate(self.board)

if __name__ == "__main__":
    p = Piece({(0,0), (1,0), (1,1)})
    p2 = Piece({(0,0), (0,1), (0,2)})
    b = Board(4)
    with b as board_state:
        board_state.place(p, (0,0), "C")
        print(board_state)
    
    with b as board_state:
        board_state.place(p2, (0,1), "Y")
        print(board_state)
