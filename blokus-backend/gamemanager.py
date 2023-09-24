import itertools
import random
from threading import Lock
import util

import playerprofile

class GameManager:
    class InvalidGameState(Exception):
        pass
    
    def __init__(self, max_players, block_degree) -> None:
        self._max_players = max_players
        self._block_deg = block_degree

        self._all_pieces = util.generate_pieces(self._block_deg)

        self._player_counter = itertools.count(1)
        self.players = {}

        self._turn_iter = itertools.cycle(range(1, max_players + 1))
        self.whose_turn = 1

        self.lock = Lock()
    
    def __enter__(self):
        try:
            with self.lock:
                return self
        except:
            pass
    
    def __exit__(self, *_exc):
        pass

    def next_turn(self):
        self.whose_turn = next(self._turn_iter)
    
    def get_player_pieces(self, pid):
        try:
            return self.players[pid].pieces
        except KeyError:
            return []
    
    def add_player(self):
        if len(self.players.keys()) < self._max_players:
            pid = next(self._player_counter)
            color = (
                random.randrange(0, 0xff) << 16 |
                random.randrange(0, 0xff) << 8 |
                random.randrange(0, 0xff) << 0
            )
            pieces = self._all_pieces.copy()
            name = f"Player {pid}"
            player = playerprofile.PlayerProfile(pid, color, name, pieces)

            self.players[pid] = player

            return player
        else:
            raise GameManager.InvalidGameState("Too many players")
    
    def remove_player(self, pid):
        pass

"".join(f"{c:02x}" for c in random.choices(range(12), k=3))