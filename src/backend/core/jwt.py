from datetime import datetime, timedelta
from typing import Any, Dict

import jwt


def decode_token(token: str, secret: str) -> Dict[str, Any]:
    return jwt.decode(token, secret, algorithms=["HS256"])


def new_token(payload: Dict[str, Any], secret: str, duration: int = 86400) -> str:
    now = datetime.utcnow()

    payload["iat"] = now
    payload["exp"] = now + timedelta(seconds=duration)
    return jwt.encode(payload, secret, algorithm="HS256")
