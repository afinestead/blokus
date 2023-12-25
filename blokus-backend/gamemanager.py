from collections import deque
from enum import Enum
import itertools
from fastapi import WebSocket, WebSocketDisconnect
import random
import string
from threading import Lock
import util
from typing import Any, Dict, Optional, Set

from board import Board
from piece import Piece
from playerprofile import PlayerProfile
from socketmanager import SocketManager
import models

piece_cache: Dict[int, Set[Piece]] = dict()
cache_lock = Lock()

def get_or_generate_pieces(degree) -> Set[Piece]:
    with cache_lock:
        if pieces := piece_cache.get(degree):
            return pieces
    
    gen = util.generate_pieces(degree)
    with cache_lock:
        piece_cache[degree] = gen
    
    return gen


class GameManager:
    class InvalidGameState(Exception):
        pass
    
    class GameOver(Exception):
        pass
    
    def __init__(
        self,
        players: int,
        block_degree: int,
        board_size: int
    ) -> None:
        self._socket_manager = SocketManager()

        self._block_deg: int = block_degree

        self._all_pieces: Set[Piece] = get_or_generate_pieces(block_degree)

        self._unique_pid: Set[int] = set(range(1, players+1))
        self._taken_pid: Set[int] = set()
        self.players: Dict[int, PlayerProfile] = {}
        self._turn_iter = deque()

        self._status = models.GameStatus.WAITING

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

    async def handle_player_update(
        self,
        pid: int,
        color: Optional[int] = None,
        name: Optional[str] = None,
    ):
        player = self.players[pid]
        # TODO: validate input
        player.color = color or player.color
        player.name = name or player.name
        await self.broadcast_players_change()


    async def broadcast_players_change(self):
        await self._socket_manager.broadcast(dict(players=[
            dict(
                player_id=p.pid,
                color=p.color,
                name=p.name,
            ) for p in self.players.values()
        ]))

    async def connect_player(self, websocket: WebSocket, pid: int):
        with self.lock:
            await self._socket_manager.connect(websocket)

            # When a new user connects, send them the current game state
            await self._socket_manager.send_personal_message(websocket, dict(
                status=self._status.value,
                board=self.board.board,
                player_id=pid,
                turn=self.whose_turn,
                players=[
                    dict(
                        player_id=p.pid,
                        color=p.color,
                        name=p.name,
                    ) for p in self.players.values()
                ],
            ))

            if pid not in self._taken_pid:
                # Alert everyone of a new change to the online players
                await self._socket_manager.broadcast(dict(
                    status=self._status.value,
                    chat=dict(
                        pid="GAME",
                        msg=f"{self.players[pid].name} has joined the game",
                    ),
                    players=[
                        dict(
                            player_id=p.pid,
                            color=p.color,
                            name=p.name,
                        ) for p in self.players.values()
                    ],
                ))
                self._taken_pid.add(pid)
                
        try:
            while True:
                data: Dict[str, Any] = await websocket.receive_json()
                print(data)
                with self.lock:
                    if "update" in data:
                            await self.handle_player_update(
                                pid=pid,
                                color=data["update"].get("color"),
                                name=data["update"].get("name"),
                            )
                    if "chat" in data:
                        await self._socket_manager.broadcast(dict(chat=dict(
                            pid=pid,
                            msg=data["chat"],
                        )))

        except WebSocketDisconnect:
            with self.lock:
                self._socket_manager.disconnect(websocket)

    @property
    def whose_turn(self) -> int:
        return self._turn_iter[0]

    @property
    def board(self):
        return self._board

    @property
    def status(self):
        with self.lock:
            if self._unique_pid:
                # Waiting for other players to join
                return models.GameStatus.WAITING
            # elif game_over: TODO: check end-game scenarios
            #   return models.GameStatus.DONE
            else:
                return models.GameStatus.ACTIVE
    
    def next_turn(self):
        possible_turns = list(self._turn_iter)

        for _ in possible_turns:
            self._turn_iter.rotate(-1)
            maybe_turn = self._turn_iter[0]
            if util.has_legal_move(self.board, maybe_turn, self.players[maybe_turn].pieces):
                return maybe_turn
            # TODO: If configured to end on first out, raise GameOver here
            self._turn_iter.popleft()
        
        raise GameManager.GameOver("No more legal moves")
        
    async def place_piece(
        self,
        piece: models.Piece,
        origin: models.Coordinate,
        pid: int
    ):
        piece_internal = Piece(piece.shape)
        player = self.players[pid]
        if not (piece_match := util.find_in_set(piece_internal, player.pieces)):
            raise GameManager.InvalidGameState("Invalid piece")
        
        self.board.place(piece_internal, origin, pid)
        player.pieces.remove(piece_match)

        self.next_turn()
        
        await self._socket_manager.broadcast(dict(
            board=self.board.board,
            turn=self.whose_turn,
        ))

    def get_player_by_id(self, pid: int):
        return self.players[pid]

    def get_player_pieces(self, pid: int):
        try:
            return self.get_player_by_id(pid).pieces
        except KeyError:
            return []
    
    async def add_player(
        self,
        name: Optional[str] = None,
        color: Optional[int] = None
    ):
        with self.lock:
            if self._unique_pid:
                pid = self._unique_pid.pop()
                pieces = self._all_pieces.copy()
                name = name or f"Player {pid}"
                player = PlayerProfile(pid, color, name, pieces)

                self._turn_iter.append(pid)
                self.players[pid] = player
                
                # TODO: Find a better place to track game state
                if not self._unique_pid:
                    self._status = models.GameStatus.ACTIVE

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
        game_state = GameManager(
            players=config.players,
            block_degree=config.block_size,
            board_size=config.board_size,
        )

        game_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

        self.active_games[game_id] = game_state

        return models.GameID(game_id=game_id)
    
    async def join_game(
        self,
        game_id: models.GameID,
        name: Optional[str] = None,
        color: Optional[int] = None,
    ):
        return await self.active_games[game_id].add_player(name, color)

    def drop_game(self, game_id: models.GameID) -> None:
        self.active_games.pop(game_id)
    
    def get_game(self, game_id: models.GameID) -> GameManager:
        return self.active_games[game_id]
