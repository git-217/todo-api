from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas.users_schema import UserRegisterSchema, UserAuthSchema
from backend.app.services.user_services import UserService
from backend.app.db.session import get_async_session


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register')
async def register(new_user: UserRegisterSchema,
                            db: AsyncSession = Depends(get_async_session)):
    
    result = UserService(db).registrate_user(user_mail=new_user.email)
    if result:
        return {'msg': 'Registration success'}
    else:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists'
            )


@router.post('/login')
async def login(response: Response, 
                auth_data: UserAuthSchema,
                db: AsyncSession = Depends(get_async_session)
                ):
    user = UserService(db).login_user(data=auth_data)