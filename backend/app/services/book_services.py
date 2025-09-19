from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.books_schema import BookCreateSchema, BookResponseSchema
from backend.app.db.repositories.book_repo import book_crud_repo
from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book




class BookS:
    def __init__(self, db: AsyncSession):
        self.book_repo = book_crud_repo
        self.db = db
    
    async def create(self, *, db: AsyncSession, owner: User, book_data: BookCreateSchema) -> BookResponseSchema:
        data = book_data.model_dump()
        data.update(user=owner)
        new_book = await self.book_repo.create(db=db, obj_data=data)
        return BookResponseSchema.model_validate(new_book)
    
    async def get_book_by_id(self, *, user_id: int, book_id: int) -> BookResponseSchema | None:
        result = await book_crud_repo.get_by_id(db=self.db, id = book_id)
        if (result is None) or (not result.user.id == user_id):
            return None
        
        return BookResponseSchema.model_validate(result)

    
BookService = BookS