import jwt
import jwt.exceptions
from datetime import datetime, timedelta
from typing import Union

ALGORITHM = "HS256"


class AuthorizationError(Exception):
    pass

def create_access_token(
    pid: int,
    gid: int,
    secret_key: str | bytes,
    expires_in: int
):
    payload = {
        "player_id": pid,
        "game_id": gid,
        "exp": datetime.utcnow() + timedelta(minutes=expires_in)
    }
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)


def decode_access_token(token: Union[str, bytes], secret_key: Union[str, bytes]):
    try:
        # JWT forces strings to bytes anyway (for both tokens and keys) and appears to 
        # throw if there's an issue. (see prepare_key() in algorithms.py and _load in apt_jwt.py)
        return jwt.decode(token, secret_key, algorithms=[ALGORITHM]) # type: ignore
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise AuthorizationError
