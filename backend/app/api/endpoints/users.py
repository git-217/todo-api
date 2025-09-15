from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth import verify_password, get_password_hash
from backend.app.services.user_services import UserService
from backend.app.schemas.users_schema import UserResponseSchema
from backend.app.db.session import get_async_session


router = APIRouter(prefix='/users', tags=['User api'])


@router.get('/user/{user_id}') 
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