from threading import Lock
from typing import Tuple

import models
# from piece import Piece

class InvalidBoardState(Exception):
    pass

class Board:
    # only ever one Board object with consistent board state

    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [[None]*dimension for _ in range(dimension)]
        self.lock = Lock()
        self.onupdate = None
    
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
    
    def get_board_square(self, coord: models.Coordinate):
        return self.board[coord.y][coord.x]
    
    def set_board_square(self, coord: models.Coordinate, player_id: int):
        self.board[coord.y][coord.x] = player_id
    
    async def place(
        self,
        piece: models.Piece,
        origin: models.Coordinate,
        player_id: int
    ):  
        def occupied_by_player(coord: models.Coordinate) -> bool:
            return self.get_board_square(coord) == player_id

        def get_neighbor(coord: models.Coordinate, direction: str) -> models.Coordinate:
            if direction == "left":
                return models.Coordinate(x=coord.x-1,y=coord.y) if coord.x > 0 else None
            elif direction == "right":
                return models.Coordinate(x=coord.x+1,y=coord.y) if coord.x < self.dimension - 1 else None
            elif direction == "up":
                return models.Coordinate(x=coord.x,y=coord.y-1) if coord.y > 0 else None
            elif direction == "down":
                return models.Coordinate(x=coord.x,y=coord.y+1) if coord.y < self.dimension - 1 else None
            else:
                return None

        def has_self_side(coord: models.Coordinate):
            l = get_neighbor(coord, "left")
            r = get_neighbor(coord, "right")
            u = get_neighbor(coord, "up")
            d = get_neighbor(coord, "down")
            return (
                (l is not None and occupied_by_player(l)) or
                (r is not None and occupied_by_player(r)) or
                (u is not None and occupied_by_player(u)) or
                (d is not None and occupied_by_player(d))
            )
        
        def has_valid_corner(coord: models.Coordinate):
            ul = get_neighbor(get_neighbor(coord, "up"), "left")
            ur = get_neighbor(get_neighbor(coord, "up"), "right")
            dl = get_neighbor(get_neighbor(coord, "down"), "left")
            dr = get_neighbor(get_neighbor(coord, "down"), "right")
            return (
                (ul is not None and occupied_by_player(ul)) or
                (ur is not None and occupied_by_player(ur)) or
                (dl is not None and occupied_by_player(dl)) or
                (dr is not None and occupied_by_player(dr))
            )
        
        valid_corner = False
        for coord in piece.shape:
            abs_coord = models.Coordinate(x=origin.x+coord.x, y=origin.y+coord.y)
            if self.get_board_square(abs_coord) is not None:
                raise InvalidBoardState
            
            if has_self_side(abs_coord):
                raise InvalidBoardState
            
            valid_corner = (
                valid_corner or
                coord == models.Coordinate(x=0,y=0) or # TODO: Translate this into player coord system
                has_valid_corner(abs_coord)
            )

        if not valid_corner:
            raise InvalidBoardState
        
        # All checks pass, this is a valid board state
        for coord in piece.shape:
            abs_coord = models.Coordinate(x=origin.x+coord.x, y=origin.y+coord.y)
            self.set_board_square(abs_coord, player_id)

        await self.onupdate()
