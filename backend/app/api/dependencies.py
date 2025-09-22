from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from backend.app.db.session import get_async_session
from backend.app.core.config import get_auth_data
from backend.app.services.user_services import UserService
from backend.app.db.models.users_models import User
from backend.app.tools.enums import UserRoles


def get_token(request: Request):
    token = request.cookies.get('user_access_token')

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    return token


async def get_current_user(token: str = Depends(get_token), db: AsyncSession = Depends(get_async_session)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token=token, 
                             key=auth_data['secret_key'],
                             algorithms=auth_data['algorithm'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return await UserService(db).get_user_by_id_full(int(user_id))


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role is UserRoles.ADMIN:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail='Access denied')