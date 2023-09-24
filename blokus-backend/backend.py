import asyncio
import itertools
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Set

import board
import gamemanager
import models
import util
import piece

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_state = gamemanager.GameManager(2, 5)
game_board = board.Board(20)
player_counter = itertools.count(1)
players = []

async def handle_board_update(board):
    await manager.broadcast(dict(board=board))

async def handle_players_change():
    await manager.broadcast(dict(players=[
        dict(
            player_id=p.pid,
            color=p.color,
            name=p.name,
        ) for p in game_state.players.values()
    ]))


@app.get("/")
async def root():
    return {"message": "yup"}

@app.post("/start")
async def start_game():
    pass

@app.get(
    "/pieces",
    response_model=List[models.Piece]
)
async def get_pieces(pid: int):
    pieces = game_state.get_player_pieces(pid)
    return [models.Piece(shape={models.Coordinate(x=x,y=y) for x,y in piece}) for piece in pieces]


@app.put("/place", response_class=JSONResponse)
async def place_piece(
    player_id: int,
    piece: models.Piece,
    origin: models.Coordinate
):
    try:
        with game_state:
            # if game_state.whose_turn != player_id:
            #     return JSONResponse(status_code=409, content="Not your turn silly")
            with game_board:
                await game_board.place(piece, origin, player_id)
                await handle_board_update(game_board.board)
                game_state.next_turn()

        return JSONResponse(status_code=200, content="Board updated")
    except board.InvalidBoardState:
        return JSONResponse(status_code=400, content="Invalid placement")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
update_queue = asyncio.Queue()

@app.websocket("/ws")
async def game(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        new_player = game_state.add_player()
    except gamemanager.GameManager.InvalidGameState:
        await manager.disconnect(websocket)

    # When a new user connects, send them the current game state
    with game_board:
        await manager.send_personal_message(websocket, dict(
            player_id=new_player.pid,
            board=game_board.board
        ))
        await handle_players_change()
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
