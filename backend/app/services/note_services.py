from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.repositories.book_repo import book_crud_repo
from backend.app.db.repositories.user_repo import user_crud_repo
from backend.app.db.repositories.note_repo import note_crud_repo
from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book
from backend.app.db.models.notes_models import Note
from backend.app.schemas.notes_schema import (NoteCreateSchema, 
                                              NoteUpdateSchema,
                                              NoteReadSchema)
from backend.app.tools.exceptions import (NotFoundException, 
                                         ConflictException, 
                                         ForbiddenException)

class NoteService:
    def __init__(self, db: AsyncSession):
        self.note_repo = note_crud_repo
        self.book_repo = book_crud_repo
        self.user_repo = user_crud_repo
        self.db = db

    async def create_note(self, 
                          *, 
                          owner: User, 
                          book_id: int, 
                          note_data: NoteCreateSchema
                          ) -> NoteReadSchema:
        current_book = await self.book_repo.get_by_id(db=self.db, id=book_id)
        if not current_book:
            raise NotFoundException("Current book doesn't exist")
        if current_book.author_id != owner.id:
            raise ForbiddenException("Not your book")
               

        note = note_data.model_dump()
        note.update(user=owner, book=current_book)
        
        note = await self.note_repo.create(db=self.db, obj_data=note)
        if note is None:
            raise ConflictException("Failed to create note")
        return NoteReadSchema.model_validate(note)