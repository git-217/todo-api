from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.book_repo import book_crud_repo
from backend.app.schemas.books_schema import BookCreateSchema, BookResponseSchema
from backend.app.repositories.user_repo import user_crud_repo




class Book:
    def __init__(self):
        self.book_repo = book_crud_repo
        self.user_repo = user_crud_repo
    
    async def create(self, *, db: AsyncSession, book_data: BookCreateSchema) -> BookResponseSchema:
        data = book_data.model_dump()
        new_book = await self.book_repo.create(db=db, obj_data=data)
        return BookResponseSchema.model_dump(new_book)
    
    async def get(self, *, db: AsyncSession, user_id: int, book_id: int) -> BookResponseSchema | None:
        result = book_crud_repo.get(book_id)
        if not result.user.id == user_id:
            return None
        
        return BookResponseSchema.model_dump(result)
    
    