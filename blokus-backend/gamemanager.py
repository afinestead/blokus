from collections import deque
import itertools
from fastapi import WebSocket, WebSocketDisconnect
import random
import string
from threading import Lock
import util
from typing import Dict, Set

from board import Board
from piece import Piece
from playerprofile import PlayerProfile
from socketmanager import SocketManager
import models

class GameManager:
    class InvalidGameState(Exception):
        pass
    
    def __init__(
        self,
        players: int,
        block_degree: int,
        board_size: int
    ) -> None:
        self._socket_manager = SocketManager()

        self._block_deg: int = block_degree

        self._all_pieces: Set[Piece] = util.generate_pieces(self._block_deg)

        self._unique_pid: Set[int] = set(range(1, players+1))
        self._taken_pid: Set[int] = set()
        self.players: Dict[int, PlayerProfile] = {}
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

    async def broadcast_players_change(self):
        await self._socket_manager.broadcast(dict(players=[
        dict(
            player_id=p.pid,
            color=p.color,
            name=p.name,
        ) for p in self.players.values()
    ]))

    async def connect_player(self, websocket: WebSocket, pid: int):
        print("calling connect")
        await self._socket_manager.connect(websocket)
        print("ok")
        # When a new user connects, send them the current game state
        print("locing")
        with self.lock:
            print("locked")
            await self._socket_manager.send_personal_message(websocket, dict(
                board=self.board.board,
                player_id=pid,
            ))
            # Also alert everyone else of a new change to the online players
            await self.broadcast_players_change()
        print("done with lock")
        try:
            while True:
                data = await websocket.receive_text()
                print(data)
                # TODO: Use data from client
        except WebSocketDisconnect:
            self._socket_manager.disconnect(websocket)

    @property
    def whose_turn(self):
        return self._turn_iter[0]

    @property
    def board(self):
        return self._board

    def next_turn(self):
        self._turn_iter.rotate(-1)
    
    async def place_piece(
        self,
        piece: models.Piece,
        origin: models.Coordinate,
        player_id: int
    ):
        self.board.place(piece, origin, player_id)
        await self._socket_manager.broadcast(dict(board=self.board.board))
    
    def get_player_by_id(self, pid: int):
        return self.players[pid]

    def get_player_pieces(self, pid: int):
        try:
            return self.get_player_by_id(pid).pieces
        except KeyError:
            return []
    
    def add_player(self):
        with self.lock:
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
                player = PlayerProfile(pid, color, name, pieces)

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


class GameServer:
    def __init__(self):
        # self.join_tokens: Dict[str] = 
        self.active_games: Dict[models.GameID, GameManager] = {}

    def create_game(self, config: models.GameConfig) -> models.GameID:
        print(config)
        game_state = GameManager(
            players=config.players,
            block_degree=config.block_size,
            board_size=config.board_size,
        )

        game_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

        self.active_games[game_id] = game_state

        return models.GameID(game_id=game_id)
    
    def join_game(self, game_id: models.GameID):
        return self.active_games[game_id].add_player()

    def drop_game(self, game_id: models.GameID) -> None:
        self.active_games.pop(game_id)
    
    def get_game(self, game_id: models.GameID) -> GameManager:
        return self.active_games[game_id]
