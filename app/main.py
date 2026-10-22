from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.api import users
from app.api import auth, users

app = FastAPI(title="Knowledge Hub")
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/healt")
async def healt(session: AsyncSession = Depends(get_session)):
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}



@app.get("/ping")
async def ping(session: AsyncSession = Depends(get_session)):
    return {"ping": "pong"}