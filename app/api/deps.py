from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User


oauth2PB_scheme =OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user( # возвращает нужного юзера по его токену и проверяет активный ли аккаунт
        token: str = Depends(oauth2PB_scheme),
        session: AsyncSession = Depends(get_session),
) -> User:
    credentials_error = HTTPException( # возвращает юзеру ошибку в таком формате
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


    user_id = decode_access_token(token) # срабатывает если юзера нет в бд
    if user_id is None:
        raise credentials_error

    user = await session.get(User, user_id) # срабатывает если аккаунт существует, но он неактивен
    if user is None or not user.is_active:
        raise credentials_error


    return user