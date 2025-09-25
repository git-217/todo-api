from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
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


    async def get_list(self, db: AsyncSession, owner_id: int) -> list[Book]:
        query = select(Book).where(Book.author_id == owner_id)
        result = await db.execute(query)
        return result.scalars()


    async def get_book_with_notes(self,
                                  *, 
                                  db: AsyncSession, 
                                  book_id: int) -> Book:
        result = await db.execute(
            select(Book)
            .options(selectinload(Book.notes))
            .where(Book.id == book_id)
        )
        return result.scalar_one_or_none()
    
    async def autochange_book_stat(self, db:AsyncSession, book_id: int):
        book = self.get_book_with_notes(db=db, book_id=book_id)

        total_notes = len(book.notes)
        unfinished_notes = sum(1 for note in book.notes if note.status != CompleteStatus.COMPLETED)

        if total_notes == 0:
            new_status = CompleteStatus.EMPTY

        elif unfinished_notes == 0:
            new_status = CompleteStatus.COMPLETED
            
        else:
            new_status = CompleteStatus.IN_PROGRESS

        book.status = new_status

    

book_crud_repo = BookCRUDRepo(Book)