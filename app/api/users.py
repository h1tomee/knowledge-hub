from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED) # регистрация юзера
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    email = data.email.lower()

    result = await session.execute(select(User).where(User.email == email)) # проверка наличия вводимой почты на ее наличие в бд
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = User(email=email, hashed_password = hash_password(data.password)) # добавление в дб юзера если прошлая функция не отработала
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
