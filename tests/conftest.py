import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import app.models  # noqa: F401
from app.core.config import settings
from app.db.session import Base, get_session
from app.main import app


TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}_test" # бд для тестов
)



@pytest.fixture
async def client():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass = NullPool) # пустой пул соединений

    async with engine.begin() as conn: # создает копию основной бд
        await conn.run_sync(Base.metadata.create_all)


    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_session(): # своя версия фабрики сессий
        async with session_maker() as session:
            yield session


    app.dependency_overrides[get_session] = override_get_session # подставляет под эндпоинты нашу версию get_session


    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test" # тестовый http клиент
    ) as test_client:
        yield test_client


    app.dependency_overrides.clear() # очищение бд после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()