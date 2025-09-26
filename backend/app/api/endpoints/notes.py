from fastapi import APIRouter, Depends
from backend.app.db.models.users_models import User
from backend.app.api.dependencies import get_current_user, get_note_service
from backend.app.services.note_services import NoteService
from backend.app.schemas.response_schema import *
from backend.app.schemas.notes_schema import (NoteCreateSchema,
                                              NoteReadSchema,
                                              NoteUpdateSchema)
from backend.app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 PostResponseBase,
                                                 PutResponseBase,
                                                 GetListResponseBase,
                                                 DeleteResponseBase
                                                )



router = APIRouter(prefix='/notes')


@router.post('/{book_id}/note/new')
async def create_new_note(book_id: int,
                          note_data: NoteCreateSchema,
                          note_service: NoteService = Depends(get_note_service),
                          user: User = Depends(get_current_user),
                          ) -> PostResponseBase[NoteReadSchema]:
    new_note = await note_service.create_note(owner=user, 
                                                 book_id=book_id,
                                                 note_data=note_data)
    return create_response(data=new_note)


@router.get('/{book_id}/note/{note_id}')
async def get_book_note(book_id: int,
                         note_id: int,
                         note_service: NoteService = Depends(get_note_service),
                         user: User = Depends(get_current_user)
                         ) -> GetResponseBase[NoteReadSchema]:
    note = await note_service.get_one(owner=user, 
                                         book_id=book_id, 
                                         note_id=note_id)
    return create_response(data=note)

@router.get('/{book_id}/notes')
async def get_all_book_notes(book_id: int,
                             note_service: NoteService = Depends(get_note_service),
                             user: User = Depends(get_current_user)
                             ) -> GetListResponseBase[NoteReadSchema]:
    notes = await note_service.get_all(owner=user, book_id=book_id)
    return create_response(data=notes)

@router.put('/book_id/note/{note_id}')
async def change_note_data(book_id: int,
                           note_id: int,
                           note_data: NoteUpdateSchema,
                           note_service: NoteService = Depends(get_note_service),
                           user: User = Depends(get_current_user)
                           ) -> PutResponseBase[NoteReadSchema]:
    note = await note_service.update(owner=user, 
                                        book_id=book_id,
                                        note_id=note_id,
                                        note_data=note_data)
    return create_response(data=note)

@router.delete('/{book_id}/note/{note_id}')
async def delete_note(book_id: int,
                      note_id: int,
                      note_service: NoteService = Depends(get_note_service),
                      user: User = Depends(get_current_user)
                      ) -> DeleteResponseBase[NoteReadSchema]:
    deleted_note = await note_service.delete(owner=user,
                                          book_id=book_id,
                                          note_id=note_id)
    return create_response(deleted_note)