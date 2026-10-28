from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import Token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token) # вход юзера по паролю и ранее созданому логину -> возвращает токен
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    email = form.username.lower()


    result = await session.execute(select(User).where(User.email == email)) # ищет юзера в бд
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form.password, user.hashed_password): # срабатывает если пароль неверный 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active: # срабатывает если аккунт юзера не активен
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "User is inactivate"
        )

    return Token(access_token=create_access_token(user.id))