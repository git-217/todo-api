from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy import update as sqlalchemy_update

from backend.app.db.models.books_models import Book
from backend.app.db.models.users_models import User
from backend.app.db.models.notes_models import Note
from backend.app.tools.enums import CompleteStatus
from backend.app.db.repositories.base_repo import CRUDBase
from backend.app.schemas.books_schema import BookCreateSchema, BookUpdateSchema



class BookCRUDRepo(CRUDBase[Book, BookCreateSchema, BookUpdateSchema]):
    async def get_by_title(self, db: AsyncSession, title: str) -> Book:
        query = select(Book).where(Book.title == title)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, db: AsyncSession, owner_id: int, book_id: int) -> Book:
        query = select(Book).where(Book.author_id == owner_id, Book.id == book_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def change_book_status(self, db: AsyncSession, book_id: int):
        result = await db.execute(
            select(func.count(Note.id))
            .where(Note.book_id == book_id, Note.status != CompleteStatus.COMPLETED)
        )
        unfinished_notes = result.scalar_one()
        new_status = CompleteStatus.COMPLETED if unfinished_notes == 0 else CompleteStatus.IN_PROGRESS
        await db.execute(
            sqlalchemy_update(Book)
            .where(Book.id == book_id).values(Book.status == new_status)
        )

    async def update(self, *, db: AsyncSession, 
                     owner_id: int,
                     book_id: int, 
                     new_book_data: BookUpdateSchema) -> int:
        new_obj = (
            sqlalchemy_update(Book)
            .where(Book.author_id == owner_id, Book.id == book_id)
            .values(new_book_data.model_dump(exclude_unset=True))
            .execution_options(synchronize_session='fetch')
        )
        result = await db.execute(new_obj)
        return result.rowcount

book_crud_repo = BookCRUDRepo(Book)