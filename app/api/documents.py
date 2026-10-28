from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_session
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentRead


router = APIRouter(prefix="/documents", tags=["documents"])


ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt"}


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED) # отправка додкумента из доступных форматов
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS: # срабатывает если формат не тот что в одобренных
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only .pdf, .md and .txt are allowed",
        )


    content = await file.read()
    if len(content) == settings.max_upload_md * 1024 * 1024: # срабатывает если файл больше дозволенного
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"File is longer than {settings.max_upload_md} mb",
        )

    document = Document(user_id = current_user.id, filename = filename) # добавляет в сессию документ, но не загружает его в библиотеку юзера
    session.add(document)
    await session.flush()


    user_dir = Path(settings.upload_dir) / str(current_user.id) # создает директиреторию для библиотеки юзера
    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / f"{document.id}{extension}").write_bytes(content)

    await session.commit() # если все отработало штатно, то документ уходит а библиотеку юзера
    await session.refresh(document)
    return document



@router.get("", response_model=list[DocumentRead]) # возвращает список документов юзера в списке
async def list_documents(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute( # получает данные из бд 
        select(Document)
        .where(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc()) # возвращает данные по убыванию от времени создания
    )

    return result.scalars().all() # возвращает список документов