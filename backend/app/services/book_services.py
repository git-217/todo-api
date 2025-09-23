from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.books_schema import (BookCreateSchema,
                                              BookUpdateSchema,
                                              BookReadSchema)
from backend.app.db.repositories.book_repo import book_crud_repo
from backend.app.db.repositories.user_repo import user_crud_repo
from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book
from backend.app.tools.exceptions import (NotFoundException, 
                                         ConflictException, 
                                         ForbiddenException)
from backend.app.tools.enums import CompleteStatus, UserRoles



class BookService:
    def __init__(self, db: AsyncSession):
        self.book_repo = book_crud_repo
        self.user_repo = user_crud_repo
        self.db = db
    
    async def create(self, *, owner: User, book_data: BookCreateSchema) -> BookReadSchema:
        data = book_data.model_dump()
        data.update(author_id=owner.id)
        new_book = await self.book_repo.create(db=self.db, obj_data=data)
        if new_book is None:
            raise ConflictException("Failed to create book")
        return BookReadSchema.model_validate(new_book)
    
    async def get_all_books(self, owner_id: int) -> list[BookReadSchema]:
        books = await self.book_repo.get_list(db=self.db, owner_id=owner_id)
        if books is None:
            raise NotFoundException(detail='Zero books found')
        return books

    async def get_book_by_id(self, *, owner_id: int, book_id: int) -> BookReadSchema:
        book = await self.book_repo.get_by_id(db=self.db, id=book_id)
        if not book:
            raise NotFoundException('Book not found')
        if book.author_id != owner_id:
            raise ForbiddenException("Not your book")  
        return BookReadSchema.model_validate(book)


    async def update_book_data(self, *, owner: User, book_data: BookUpdateSchema) -> BookReadSchema:
        book = await self.book_repo.get_by_id(db=self.db, id=book_data.id)
        if not book:
            raise NotFoundException('Book not found')
        if (book.author_id != owner.id) or (owner.role != UserRoles.ADMIN):
            return ForbiddenException("Not your book")
        result = await self.book_repo.update(db=self.db, 
                                         id=book_data.id, 
                                         new_data_obj=book_data) 
        if result is None:
            raise ConflictException("Failed to update book")
        return book
    

    async def delete_book(self, *, owner: User, book_id: int) -> BookReadSchema:
        book = await self.book_repo.get_by_id(db=self.db, id=book_id)
        if not book:
            raise NotFoundException("Book doesn't exist")
        if (book.author_id != owner.id) or (owner.role != UserRoles.ADMIN):
            return ForbiddenException("Not your book")
        result = await self.book_repo.delete(db=self.db, id=BookUpdateSchema.id)
        if result is None:
            raise ConflictException("Failed to delete book")
        return book