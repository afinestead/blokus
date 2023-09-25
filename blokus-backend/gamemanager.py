from collections import deque
import itertools
import random
from threading import Lock
import util

from board import Board
import playerprofile

class GameManager:
    class InvalidGameState(Exception):
        pass
    
    def __init__(self, players, block_degree, board_size) -> None:
        self._max_players = players
        self._block_deg = block_degree

        self._all_pieces = util.generate_pieces(self._block_deg)

        self._unique_pid = set(range(1, players+1))
        self._taken_pid = set()
        self.players = {}
        self._turn_iter = deque()

        self._board = Board(board_size)

        self.lock = Lock()
    
    def __enter__(self):
        try:
            with self.lock:
                return self
        except:
            pass
    
    def __exit__(self, *_exc):
        pass

    @property
    def whose_turn(self):
        return self._turn_iter[0]

    @property
    def board(self):
        return self._board

    def next_turn(self):
        self._turn_iter.rotate(-1)
    
    def get_player_pieces(self, pid):
        try:
            return self.players[pid].pieces
        except KeyError:
            return []
    
    def add_player(self):
        if self._unique_pid:
            pid = self._unique_pid.pop()
            self._taken_pid.add(pid)
            color = (
                random.randrange(0, 0xff) << 16 |
                random.randrange(0, 0xff) << 8 |
                random.randrange(0, 0xff) << 0
            )
            pieces = self._all_pieces.copy()
            name = f"Player {pid}"
            player = playerprofile.PlayerProfile(pid, color, name, pieces)

            self._turn_iter.append(pid)
            self.players[pid] = player

            return player
        else:
            raise GameManager.InvalidGameState("Too many players")
    
    def remove_player(self, pid):
        print(f"removing {pid}")
        self.players.pop(pid)
        self._turn_iter.remove(pid)
        self._taken_pid.remove(pid)
        self._unique_pid.add(pid)


"".join(f"{c:02x}" for c in random.choices(range(12), k=3))