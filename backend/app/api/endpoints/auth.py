from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas.users_schema import UserRegisterSchema, UserAuthSchema
from backend.app.services.user_services import UserService
from backend.app.db.session import get_async_session


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register')
async def register(new_user: UserRegisterSchema,
                            db: AsyncSession = Depends(get_async_session)):
    
    result = await UserService(db).registrate_user(user_data=new_user)
    if result:
        print(result)
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
    access_token = await UserService(db).login_user(user_data=auth_data)
    if access_token:
        response.set_cookie(key='user_access_token', value=access_token, httponly=True)
        #refresh token realization will be somwhere in the future ig
        return {'access_token': access_token, 'refresh_token': None }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong Email or password'
        )