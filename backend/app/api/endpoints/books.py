from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user, get_book_service
from app.schemas.books_schema import (BookCreateSchema,
                                              BookUpdateSchema,
                                              BookReadSchema)
from app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 PostResponseBase,
                                                 GetListResponseBase,
                                                 PatchResponseBase,
                                                 DeleteResponseBase
                                                )
from app.services.book_services import BookService


router = APIRouter(prefix='/books', tags=['Book api'])

@router.get('/{book_id}')
async def get_book_by_id(book_id: int,
                               user = Depends(get_current_user),
                               book_service: BookService = Depends(get_book_service)
                               ) -> GetResponseBase[BookReadSchema]:
    book = await book_service.get_book_by_id(owner=user, book_id=book_id)
    return create_response(data=book)


@router.get('/', summary="Get all user's books")
async def get_users_books(user = Depends(get_current_user),
                          book_service: BookService = Depends(get_book_service)
                          ) -> GetListResponseBase[BookReadSchema]:
    books = await book_service.get_all_books(owner=user)
    books_schemas = [BookReadSchema.model_validate(b) for b in books]
    return create_response(data = books_schemas)


@router.post('/new')
async def create_new_book(book_data: BookCreateSchema,
                          user = Depends(get_current_user),
                          book_service: BookService = Depends(get_book_service)
                          ) -> PostResponseBase[BookReadSchema]:
    new_book = await book_service.create(owner=user, book_data=book_data)
    return create_response(data=new_book)

@router.patch('/update')
async def change_book_data(new_book_data: BookUpdateSchema,
                           user = Depends(get_current_user),
                           book_service: BookService = Depends(get_book_service)
                           ) -> PatchResponseBase[BookUpdateSchema]:
    updated_book = await book_service.update_book_data(owner=user, book_data=new_book_data)
    return create_response(data=updated_book)


@router.delete('/{book_id}')
async def delete_book(book_id: int,
                      user = Depends(get_current_user),
                      book_service: BookService = Depends(get_book_service)
                      ) -> DeleteResponseBase[BookReadSchema]:
    deleted_book = await book_service.delete_book(owner=user, book_id=book_id)
    return create_response(data=deleted_book)