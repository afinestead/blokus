import asyncio
import itertools
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    Response,
    Security,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status as FastAPIStatus,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from os import urandom
from typing import Annotated, Any, Dict, List, Mapping, Optional, Union

import authorization
import board
from gamemanager import GameManager, GameServer
import models
import util
import piece
from socketmanager import SocketManager

SECRET_KEY = urandom(32)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_manager = SocketManager()
game_server = GameServer()

ResponseTypeType = Mapping[Union[int, str], Dict[str, Any]]
InvalidCredentialsResponseType: ResponseTypeType = {
    401: {"description": "Invalid credentials", "model": models.Message}
}
class InvalidCredentialsException(Exception):
    pass


def verify_player_token(
    token_header: Annotated[str | None, Header()] = None,
    token_query: Annotated[str | None, Query()] = None,
):
    try:
        return authorization.decode_access_token(token_header, SECRET_KEY)
    except authorization.AuthorizationError:
        pass
    try:
        return authorization.decode_access_token(token_query, SECRET_KEY)
    except authorization.AuthorizationError:
        pass

    raise HTTPException(status_code=401, detail="Invalid token")


@app.post(
    "/game/create",
    response_model=models.GameID,
)
async def create_new_game(game_config: models.GameConfig):
    return game_server.create_game(game_config)

@app.post(
    "/game/{game_id}/join",
    response_model=models.AccessToken,
)
async def join_game(
    game_id: str,
    player_name: Optional[str] = None,
    color: Optional[int] = None,
):
    try:
        player_internal = await game_server.join_game(game_id, player_name, color)
        return models.AccessToken(access_token=authorization.create_access_token(
            player_internal.pid, 
            game_id, 
            SECRET_KEY,
            60,
        ))
    except KeyError:
        return JSONResponse(status_code=404, content="Unknown game") 
    except GameManager.InvalidGameState:
        return JSONResponse(status_code=409, content="Player capacity reached")

@app.get(
    "/player",
    response_model=models.PlayerProfile,
    responses={**InvalidCredentialsResponseType,},
)
async def get_current_player(
    token: Annotated[models.AccessToken, Depends(verify_player_token)],
):
    try:
        game_state = game_server.get_game(token["game_id"])
    except KeyError:
        return HTTPException(status_code=404, detail="Unknown game")
    with game_state:
        player = game_state.get_player_by_id(token["player_id"])

    return models.PlayerProfile(
        player_id=player.pid,
        color=player.color,
        name=player.name,
        pieces=[models.Piece(shape={models.Coordinate(x=x,y=y) for x,y in piece}) for piece in player.pieces]
    )


@app.get("/turn", response_model=int)
async def whose_turn(token: Annotated[models.AccessToken, Depends(verify_player_token)]):
    try:
        game_state = game_server.get_game(token["game_id"])
    except KeyError:
        return HTTPException(status_code=404, detail="Unknown game")
    with game_state:
        return game_state.whose_turn


@app.get("/state", response_model=models.GameState)
async def game_state(token: Annotated[models.AccessToken, Depends(verify_player_token)]):
    try:
        game_state = game_server.get_game(token["game_id"])
    except KeyError:
        return HTTPException(status_code=404, detail="Unknown game")
    with game_state:
        return models.GameState(status=game_state.status.value, turn=game_state.whose_turn)


@app.put("/place", response_class=JSONResponse)
async def place_piece(
    piece: models.Piece,
    origin: models.Coordinate,
    token: Annotated[models.AccessToken, Depends(verify_player_token)],
):
    try:
        game_state = game_server.get_game(token["game_id"])
    except KeyError:
        return HTTPException(status_code=404, detail="Unknown game")
    try:
        with game_state:
            if game_state.status != models.GameStatus.ACTIVE:
                return JSONResponse(status_code=409, content="Game not started")
            if game_state.whose_turn != token["player_id"]:
                return JSONResponse(status_code=409, content="Not your turn silly")
            await game_state.place_piece(piece, origin, token["player_id"])

        return JSONResponse(status_code=200, content="Board updated")
    except board.InvalidBoardState:
        return JSONResponse(status_code=400, content="Invalid placement")



@app.websocket("/ws")
async def game(
    websocket: WebSocket,
    token: Annotated[models.AccessToken, Depends(verify_player_token)],
):
    try:
        game_state = game_server.get_game(token["game_id"])
    except KeyError:
        return WebSocketException(code=FastAPIStatus.WS_1008_POLICY_VIOLATION)
    
    await game_state.connect_player(websocket, pid=token["player_id"])
    


    
