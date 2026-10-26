from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User


oauth2PB_scheme =OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2PB_scheme),
        session: AsyncSession = Depends(get_session),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error

    user = await session.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_error


    return user