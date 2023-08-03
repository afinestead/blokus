import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Set

import board
import models
import util
import piece

app = FastAPI()

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
    return [models.Piece(shape={(x,y) for x,y in piece}) for piece in pieces]


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

async def handle_board_update():
    with board:
        await manager.broadcast(board.board)

update_queue = asyncio.Queue()
board = Board(20, onupdate=handle_board_update)


@app.websocket("/ws")
async def game(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
