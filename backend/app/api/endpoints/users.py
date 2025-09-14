from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth import verify_password, get_password_hash
from backend.app.services.user_services import UserService
from backend.app.schemas.users_schema import UserResponseSchema, UserRegisterSchema
from backend.app.db.session import get_async_session


router = APIRouter(prefix='/users')


@router.get('/user/{user_id}') 
async def get_user_by_id(user_id: int, 
                  db: AsyncSession = Depends(get_async_session)
                  )-> UserResponseSchema | dict:
    u_service = UserService(db)
    user = await u_service.get_user_by_id(user_id=user_id)
    if user is None:
        return {'msg': 'user not found'}
    return user


@router.get('')
async def get_all_users(db: AsyncSession = Depends(get_async_session)) -> list[UserResponseSchema]:
    u_service = UserService(db)
    result = await u_service.get_all_users()
    return result


@router.post('/register')
async def register_new_user(new_user: UserRegisterSchema,
                            db: AsyncSession = Depends(get_async_session)):
    u_service = UserService(db)

    result = UserService.registrate_user(user_mail=new_user.email)
    if result:
        return {'msg': 'Registration success'}
    else:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )


@router.delete('{user_id}/delete')
async def delete_user_by_id(user_id: int,
                            db: AsyncSession = Depends(get_async_session)):
    u_service = UserService(db)
    result = u_service.delete_user_by_id(user_id=user_id)
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return {'msg': 'User successfully deleted'}