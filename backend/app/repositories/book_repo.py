from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.books_models import Book
from backend.app.repositories.base_repo import CRUDBase
from backend.app.schemas.books_schema import BookCreateSchema, BookUpdateSchema



class BookCRUDRepo(CRUDBase[Book, BookCreateSchema, BookUpdateSchema]):
    async def get_by_title(self, db: AsyncSession, title: str) -> Book | None:
        query = select(Book).where(Book.title == title)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    
    
book_crud_repo = BookCRUDRepo(Book)