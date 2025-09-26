from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.user_services import UserService
from backend.app.db.session import get_async_session
from backend.app.schemas.users_schema import (PatchUserNamesSchema,
                                              UserBasicSchema,
                                              UserWithBooksSchema,
                                              UserWithNotesSchema,
                                              UserFullSchema)
from backend.app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 GetListResponseBase,
                                                 PatchResponseBase,
                                                 DeleteResponseBase)
from backend.app.api.dependencies import (get_current_user, 
                                          get_current_admin_user,
                                          get_user_service)


router = APIRouter(prefix='/users', tags=['User api'])


@router.get('/{user_id}/basic') 
async def get_user_by_id(user_id: int,
                         user_service: UserService = Depends(get_user_service)
                         )-> GetResponseBase[UserBasicSchema]:
    user = await user_service.get_user_by_id_basic(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/with_books') 
async def get_user_by_id(user_id: int,
                         user_service: UserService = Depends(get_user_service)
                         )-> GetResponseBase[UserWithBooksSchema]:
    user = await user_service.get_user_by_id_with_books(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/with_notes') 
async def get_user_by_id(user_id: int,
                         user_service: UserService = Depends(get_user_service)
                         )-> GetResponseBase[UserWithNotesSchema]:
    user = await user_service.get_user_by_id_with_notes(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/full') 
async def get_user_by_id(user_id: int,
                         user_service: UserService = Depends(get_user_service)
                         )-> GetResponseBase[UserFullSchema]:
    user = await user_service.get_user_by_id_full(user_id=user_id)
    return create_response(data=user)

@router.get('/all')
async def get_users(user_service: UserService = Depends(get_user_service)
                    ) -> GetListResponseBase[UserBasicSchema]:
    result = await user_service.get_all_users()
    return create_response(data=result)

@router.get('/me')
async def get_user_current(user = Depends(get_current_user)) -> GetResponseBase[UserFullSchema]:
    return create_response(data=user)

@router.patch('/me', summary="change user's First/Last name")
async def change_user_names(new_data: PatchUserNamesSchema,
                            user = Depends(get_current_user),
                            user_service: UserService = Depends(get_user_service)
                            ) -> PatchResponseBase[UserBasicSchema]:
    patched = await user_service.update(uid=user.id, user_data=new_data)
    return create_response(data=patched, message='New user data')

@router.delete('/{user_id}/delete')
async def delete_user_by_id(user = Depends(get_current_admin_user),
                            user_service: UserService = Depends(get_user_service)
                            ) -> DeleteResponseBase[UserFullSchema]:

    deleted_user = user_service.delete_user_by_id(user_id=user.id)
    return create_response(data=deleted_user)