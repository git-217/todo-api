from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_async_session
from backend.app.api.dependencies import get_current_user
from backend.app.schemas.books_schema import BookCreateSchema
from backend.app.services.book_services import BookService


router = APIRouter(prefix='/books', tags=['Book api'])

@router.get('/{book_id}')
async def get_book_by_id(book_id: int,
                               user = Depends(get_current_user),
                               db: AsyncSession = Depends(get_async_session)):
    book = await BookService(db).get_book_by_id(user_id=user.id, book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book not found')
    ...