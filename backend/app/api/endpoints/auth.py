from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users_schema import (UserRegisterSchema, 
                                      UserAuthSchema, 
                                      UserBasicSchema)
from app.api.dependencies import get_user_service
from app.services.user_services import UserService
from app.db.session import get_async_session
from app.schemas.response_schema import create_response, PostResponseBase


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register')
async def register(new_user: UserRegisterSchema,
                   user_service: UserService = Depends(get_user_service)
                   ) -> PostResponseBase[UserBasicSchema]:
    
    result = await user_service.registrate_user(user_data=new_user)
    return create_response(data=result, message='Registration success')


@router.post('/login')
async def login(response: Response, 
                auth_data: UserAuthSchema,
                user_service: UserService = Depends(get_user_service)
                ):
    access_token = await user_service.create_access_token(user_data=auth_data)
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    #refresh token realization will be somwhere in the future ig
    return {'access_token': access_token, 'refresh_token': None }
    
@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'msg': 'logout'}