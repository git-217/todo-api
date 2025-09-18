from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth_base import verify_password, get_password_hash
from backend.app.services.user_services import UserService
from backend.app.schemas.users_schema import UserResponseSchema, UpdateUserNamesSchema
from backend.app.db.session import get_async_session
from backend.app.api.dependencies import get_current_user


router = APIRouter(prefix='/users', tags=['User api'])


@router.get('/users/{user_id}') 
async def get_user_by_id(user_id: int, 
                  db: AsyncSession = Depends(get_async_session)
                  )-> UserResponseSchema | dict:

    user = await UserService(db).get_user_by_id(user_id=user_id)
    if user is None:
        return {'msg': 'user not found'}
    return user



@router.get('')
async def get_all_users(db: AsyncSession = Depends(get_async_session)) -> list[UserResponseSchema]:
    result = await UserService(db).get_all_users()
    return result


@router.patch('/users/{user_id}')
async def change_user_names(new_data: UpdateUserNamesSchema,
                            user = Depends(get_current_user),
                            db: AsyncSession = Depends(get_async_session)
                            ) -> dict:
    user_id = user.id
    patched = await UserService(db).update(uid=user_id, user_data=new_data)
    if patched:
        return {'msg': f'succesfully updated {patched} params'}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="can't change data"
        )

@router.delete('{user_id}/delete')
async def delete_user_by_id(user_id: int,
                            db: AsyncSession = Depends(get_async_session)):

    result = UserService(db).delete_user_by_id(user_id=user_id)
    if result:
        return {'msg': 'User successfully deleted'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )