from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app.db.models.users_models import User
from backend.app.db.models.books_models import Book
from backend.app.db.models.notes_models import Note
from backend.app.db.session import get_async_session
from backend.app.api.dependencies import get_current_user
from backend.app.services.note_services import NoteService
from backend.app.schemas.response_schema import *
from backend.app.schemas.notes_schema import (NoteCreateSchema,
                                              NoteReadSchema)
from backend.app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 PostResponseBase,
                                                 PutResponseBase,
                                                 GetListResponseBase,
                                                 PatchResponseBase,
                                                 DeleteResponseBase
                                                )



router = APIRouter(prefix='/notes')


@router.post('/{book_id}/note/new')
async def create_new_note(book_id: int,
                          note_data: NoteCreateSchema,
                          db: AsyncSession = Depends (get_async_session),
                          user: User = Depends(get_current_user),
                          ) -> PostResponseBase[NoteReadSchema]:
    new_note = await NoteService(db).create_note(owner=user, 
                                                 book_id=book_id,
                                                 note_data=note_data)
    return create_response(data=new_note)


@router.get('/{book_id}/note/{note_id}')
async def get_book_notes(book_id: int,
                         note_id: int,
                         db: AsyncSession = Depends(get_async_session),
                         user: User = Depends(get_current_user)
                         ):
    note = await NoteService(db).get_one(owner=user, 
                                         book_id=book_id, 
                                         note_id=note_id)
    return create_response(data=note)