from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_async_session
from backend.app.api.dependencies import get_current_user
from backend.app.schemas.books_schema import (BookCreateSchema,
                                              BookUpdateSchema,
                                              BookReadSchema)
from backend.app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 PostResponseBase,
                                                 PutResponseBase,
                                                 PatchResponseBase,
                                                 DeleteResponseBase
                                                )
from backend.app.services.book_services import BookService


router = APIRouter(prefix='/books', tags=['Book api'])

@router.get('/{book_id}')
async def get_book_by_id(book_id: int,
                               user = Depends(get_current_user),
                               db: AsyncSession = Depends(get_async_session)
                               ) -> GetResponseBase[BookReadSchema]:
    book = await BookService(db).get_book_by_id(user_id=user.id, book_id=book_id)
    return create_response(data=book)


@router.post('/new')
async def create_new_book(book_data: BookCreateSchema,
                          user = Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)) -> PostResponseBase[BookReadSchema]:
    new_book = await BookService(db).create(owner=user, book_data=book_data)
    return create_response(data=new_book)

@router.patch('/update')
async def change_book_data(new_book_data: BookUpdateSchema,
                           user = Depends(get_current_user),
                           db: AsyncSession = Depends(get_async_session)
                           ) -> PatchResponseBase[BookUpdateSchema]:
    updated_book = await BookService(db=db).update_book_data(owner=user, book_data=new_book_data)
    return create_response(data=updated_book)