from enum import IntEnum
from threading import Lock

import models
# from piece import Piece

class InvalidBoardState(Exception):
    pass

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

def get_neighbor(
    coord: models.Coordinate,
    direction: Direction,
    min_coord: int,
    max_coord: int,
) -> models.Coordinate:
    if coord is None:
        return None
    
    if direction == Direction.UP:
        return models.Coordinate(x=coord.x-1,y=coord.y) if coord.x > min_coord else None
    elif direction == Direction.DOWN:
        return models.Coordinate(x=coord.x+1,y=coord.y) if coord.x < max_coord - 1 else None
    elif direction == Direction.LEFT:
        return models.Coordinate(x=coord.x,y=coord.y-1) if coord.y > min_coord else None
    elif direction == Direction.RIGHT:
        return models.Coordinate(x=coord.x,y=coord.y+1) if coord.y < max_coord - 1 else None
    else:
        return None

class Board:
    # only ever one Board object with consistent board state

    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [[None]*dimension for _ in range(dimension)]
        self.lock = Lock()
    
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
        
    def place(
        self,
        piece: models.Piece,
        origin: models.Coordinate,
        player_id: int
    ):  
        print(origin, piece)
        valid_corner = False
        for coord in piece.shape:
            abs_coord = models.Coordinate(x=origin.x+coord.x, y=origin.y+coord.y)
            if self.get_board_square(abs_coord) is not None:
                raise InvalidBoardState
            
            if self.has_self_side(abs_coord, player_id, max_coord=self.dimension):
                raise InvalidBoardState
            
            valid_corner = (
                valid_corner or
                coord == models.Coordinate(x=0,y=0) or
                self.has_valid_corner(abs_coord, player_id, max_coord=self.dimension)
            )

        if not valid_corner:
            raise InvalidBoardState
        
        # All checks pass, this is a valid board state
        for coord in piece.shape:
            abs_coord = models.Coordinate(x=origin.x+coord.x, y=origin.y+coord.y)
            self.board[abs_coord.x][abs_coord.y] = player_id
        
        print(self)
    

    def get_board_square(self, coord: models.Coordinate) -> int:
        print(coord.x, coord.y)
        return self.board[coord.x][coord.y]

    def occupied_by_player(self, pid: int, coord: models.Coordinate) -> bool:
        return self.get_board_square(coord) == pid


    def has_self_side(
        self,
        coord: models.Coordinate,
        pid: int,
        max_coord: int,
        min_coord: int = 0,
    ):
        
        def get_neighbor_helper(dir: Direction) -> models.Coordinate:
            return get_neighbor(coord, dir, min_coord, max_coord)

        def occupied_by_pid(coord: models.Coordinate) -> bool:
            return self.occupied_by_player(pid, coord)

        l = get_neighbor_helper(Direction.LEFT)
        r = get_neighbor_helper(Direction.RIGHT)
        u = get_neighbor_helper(Direction.UP)
        d = get_neighbor_helper(Direction.DOWN)
        return (
            (l is not None and occupied_by_pid(l)) or
            (r is not None and occupied_by_pid(r)) or
            (u is not None and occupied_by_pid(u)) or
            (d is not None and occupied_by_pid(d))
        )

    def has_valid_corner(
        self,
        coord: models.Coordinate,
        pid: int,
        max_coord: int,
        min_coord: int = 0,
    ):
        def get_neighbor_helper(coord, dir: Direction) -> models.Coordinate:
            return get_neighbor(coord, dir, min_coord, max_coord)

        def occupied_by_pid(coord: models.Coordinate) -> bool:
            return self.occupied_by_player(pid, coord)

        ul = get_neighbor_helper(get_neighbor_helper(coord, Direction.UP), Direction.LEFT)
        ur = get_neighbor_helper(get_neighbor_helper(coord, Direction.UP), Direction.RIGHT)
        dl = get_neighbor_helper(get_neighbor_helper(coord, Direction.DOWN), Direction.LEFT)
        dr = get_neighbor_helper(get_neighbor_helper(coord, Direction.DOWN), Direction.RIGHT)
        return (
            (ul is not None and occupied_by_pid(ul)) or
            (ur is not None and occupied_by_pid(ur)) or
            (dl is not None and occupied_by_pid(dl)) or
            (dr is not None and occupied_by_pid(dr))
        )
