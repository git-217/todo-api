from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.tools.enums import CompleteStatus
from backend.app.db.repositories.book_repo import book_crud_repo
from backend.app.db.repositories.note_repo import note_crud_repo
from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book
from backend.app.schemas.notes_schema import (NoteCreateSchema, 
                                              NoteUpdateSchema,
                                              NoteReadSchema)
from backend.app.tools.exceptions import (NotFoundException,
                                         ForbiddenException)

class NoteService:
    def __init__(self, db: AsyncSession,
                 note_repo = note_crud_repo,
                 book_repo = book_crud_repo):
        self.note_repo = note_repo
        self.book_repo = book_repo
        self.db = db
    
    async def _validate_permissions(self, 
                                    owner_id: int,
                                    book_id: int,
                                    note_id=int | None) -> Book:
        book = await self.book_repo.get_book_with_notes(db=self.db, book_id=book_id)
        if not book:
            raise NotFoundException("Book not found")
        if book.author_id != owner_id:
            raise ForbiddenException("Not your book")
        if note_id and (note_id not in book.notes):
            raise NotFoundException("Note not found")
        return book

    async def create_note(self, 
                          *, 
                          owner: User, 
                          book_id: int, 
                          note_data: NoteCreateSchema
                          ) -> NoteReadSchema:
        await self._validate_permissions(owner_id=owner.id, 
                                         book_id=book_id,
                                         note_id=note_data.id)

        note = await self.note_repo.create(db=self.db, obj_data=note_data, 
                                           author_id=owner.id, 
                                           book_id=book_id)

        await self.book_repo.autochange_book_stat(db=self.db, book_id=book_id)

        return NoteReadSchema.model_validate(note)
    
    async def get_one(self,
                      *,
                      owner: User,
                      book_id: int,
                      note_id: int
                      ) -> NoteReadSchema:
        
        await self._validate_permissions(owner_id=owner.id, 
                                         book_id=book_id,
                                         note_id=note_id)
        
        note = await self.note_repo.get_by_id(db=self.db, id=note_id)
        if note is None:
            raise NotFoundException("Note doesn't exist")
        return NoteReadSchema.model_validate(note)
    
    async def get_all(self,
                      *,
                      owner: User,
                      book_id: int,
                      ) -> list[NoteReadSchema]:
        
        await self._validate_permissions(owner_id=owner.id, book_id=book_id)

        notes = await self.note_repo.get_list(db=self.db)
        if notes is None:
            raise NotFoundException('Current book is empty')
        return [NoteReadSchema.model_validate(note) for note in notes]

    async def update(self, *,
                     owner: User,
                     book_id: int,
                     note_id: int,
                     note_data: NoteUpdateSchema
                     ) -> NoteReadSchema:
        await self._validate_permissions(owner_id=owner.id, book_id=book_id)

        updated_note = await self.note_repo.update(
                                                   db=self.db,
                                                   id=note_id,
                                                   new_data_obj=note_data
                                                  )
        if not updated_note:
            raise NotFoundException('Note not found')
        
        return NoteReadSchema.model_validate(updated_note)
    
    async def delete(self, *,
                     owner: User,
                     book_id: int,
                     note_id: int
                     ) -> NoteReadSchema:
        await self._validate_permissions(owner_id=owner.id, book_id=book_id)

        deleted_note = await self.note_repo.delete(db=self.db, id=note_id)
        if deleted_note is None:
            raise NotFoundException("Note not found")
        
        await self.book_repo.autochange_book_stat(db=self.db, book_id=book_id)
        
        return NoteReadSchema.model_validate(deleted_note)