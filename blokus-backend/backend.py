import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Set

import board
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

game_board = board.Board(20)

async def handle_board_update(board):
    await manager.broadcast(dict(board=board))


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
async def get_pieces(degree: int):
    pieces = util.generate_pieces(degree)
    for piece in pieces:
        print(piece)
    return [models.Piece(shape={models.Coordinate(x=x,y=y) for x,y in piece}) for piece in pieces]


@app.put("/place", response_class=JSONResponse)
async def place_piece(
    player_id: int,
    piece: models.Piece,
    origin: models.Coordinate
):
    try:
        with game_board:
            await game_board.place(piece, origin, player_id)
            await handle_board_update(game_board.board)
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
        print("Broadcasting update")
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
update_queue = asyncio.Queue()

@app.websocket("/ws")
async def game(websocket: WebSocket):
    await manager.connect(websocket)
    # When a new user connects, send them the current game state
    with game_board:
        await manager.send_personal_message(websocket, dict(board=game_board.board))
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
