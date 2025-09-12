from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import services
from backend.app.schemas.users_schema import UserGetSchema, UserRegisterSchema
from backend.app.db.session import get_async_session


router = APIRouter(prefix='/users')


@router.get('/{user_id}') 
async def get_user_by_id(user_id: int, 
                  db: AsyncSession = Depends(get_async_session)
                  )-> UserGetSchema | dict:
    u_service = services.user_services.User(db)
    user = await u_service.get_user_by_id(user_id=user_id)
    if user is None:
        return {'msg': 'user not found'}
    return user


@router.post('/register')
async def register_new_user(new_user: UserRegisterSchema,
                            db: AsyncSession = Depends(get_async_session)):
    u_service = services.user_services.User(db)
    result = await u_service.create_user(new_user)
    if result is None:
        return {"msg": "user creating error"}
    return {'msg': f"created user with ID: {result.id}"}