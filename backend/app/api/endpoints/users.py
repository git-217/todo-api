from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.user_services import UserService
from backend.app.schemas.users_schema import (UserRegisterSchema,
                                              PatchUserNamesSchema,
                                              UserUpdateSchema, 
                                              UserBasicSchema,
                                              UserWithBooksSchema,
                                              UserWithNotesSchema,
                                              UserAuthSchema,
                                              UserFullSchema)
from backend.app.db.session import get_async_session
from backend.app.db.models.users_models import User
from backend.app.schemas.response_schema import (create_response,
                                                 GetResponseBase,
                                                 PostResponseBase,
                                                 PutResponseBase,
                                                 GetListResponseBase,
                                                 PatchResponseBase,
                                                 DeleteResponseBase
                                                )

from backend.app.api.dependencies import get_current_user, get_current_admin_user


router = APIRouter(prefix='/users', tags=['User api'])


@router.get('/{user_id}/basic') 
async def get_user_by_id(user_id: int,
                         db: AsyncSession = Depends(get_async_session)
                         )-> GetResponseBase[UserBasicSchema]:
    user = await UserService(db).get_user_by_id_basic(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/with_books') 
async def get_user_by_id(user_id: int,
                         db: AsyncSession = Depends(get_async_session)
                         )-> GetResponseBase[UserWithBooksSchema]:
    user = await UserService(db).get_user_by_id_with_books(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/with_notes') 
async def get_user_by_id(user_id: int,
                         db: AsyncSession = Depends(get_async_session)
                         )-> GetResponseBase[UserWithNotesSchema]:
    user = await UserService(db).get_user_by_id_with_notes(user_id=user_id)
    return create_response(data=user)

@router.get('/{user_id}/full') 
async def get_user_by_id(user_id: int,
                         db: AsyncSession = Depends(get_async_session)
                         )-> GetResponseBase[UserFullSchema]:
    user = await UserService(db).get_user_by_id_full(user_id=user_id)
    return create_response(data=user)

@router.get('/all')
async def get_users(db: AsyncSession = Depends(get_async_session)) -> GetListResponseBase[UserBasicSchema]:
    result = await UserService(db).get_all_users()
    return create_response(data=result)

@router.get('/me')
async def get_user_current(user = Depends(get_current_user)) -> GetResponseBase[UserFullSchema]:
    return create_response(data=user)

@router.patch('/me', summary="change user's First/Last name")
async def change_user_names(new_data: PatchUserNamesSchema,
                            user = Depends(get_current_user),
                            db: AsyncSession = Depends(get_async_session)
                            ) -> PatchResponseBase[UserBasicSchema]:
    patched = await UserService(db).update(uid=user.id, user_data=new_data)
    return create_response(data=patched, message='New user data')

@router.delete('/{user_id}/delete')
async def delete_user_by_id(user = Depends(get_current_admin_user),
                            db: AsyncSession = Depends(get_async_session)
                            ) -> DeleteResponseBase[UserFullSchema]:

    deleted_user = UserService(db).delete_user_by_id(user_id=user.id)
    return create_response(data=deleted_user)