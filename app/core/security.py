from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str: # хэширование пароля
    return password_hash.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool: # проверка пароля с уже хэшированным
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire =datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.PyJWTError:
        return None
    return int(payload["sub"])