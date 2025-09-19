from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.books_schema import (BookCreateSchema, 
                                              BookResponseSchema,
                                              BookUpdateSchema)
from backend.app.db.repositories.book_repo import book_crud_repo
from backend.app.db.repositories.user_repo import user_crud_repo
from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book




class BookS:
    def __init__(self, db: AsyncSession):
        self.book_repo = book_crud_repo
        self.user_repo = user_crud_repo
        self.db = db
    
    
    async def create(self, *, owner: User, book_data: BookCreateSchema) -> BookResponseSchema:
        data = book_data.model_dump()
        data.update(user=owner)
        new_book = await self.book_repo.create(db=self.db, obj_data=data)
        return BookResponseSchema.model_validate(new_book)
    

    async def get_book_by_id(self, *, user_id: int, book_id: int) -> BookResponseSchema | None:
        result = await book_crud_repo.get_by_id(db=self.db, owner_id=user_id, book_id=book_id)
        if result is None:
            return None      
        return BookResponseSchema.model_validate(result)


    async def update_book_data(self, *, owner: User, book_data: BookUpdateSchema) -> int:
        result = await self.book_repo.update(db=self.db, 
                                         owner_id=owner.id, 
                                         book_id=book_data.id, 
                                         new_book_data=book_data) 
        if result is None:
            return None
        return result

        

BookService = BookS