from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.tools.enums import UserRoles
from app.core.config import get_auth_data
from app.db.session import get_async_session
from app.db.models.users_models import User
from app.services.user_services import UserService
from app.services.book_services import BookService
from app.services.note_services import NoteService
from app.schemas.users_schema import UserFullSchema
from app.db.repositories.user_repo import user_crud_repo
from app.db.repositories.book_repo import book_crud_repo
from app.db.repositories.note_repo import note_crud_repo


async def get_user_service(
    db: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(db=db, user_repo=user_crud_repo)


async def get_book_service(
    db: AsyncSession = Depends(get_async_session),
) -> BookService:
    return BookService(db=db, book_repo=book_crud_repo)


async def get_note_service(
    db: AsyncSession = Depends(get_async_session),
) -> NoteService:
    return NoteService(db=db, note_repo=note_crud_repo, book_repo=book_crud_repo)


def get_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_current_user(
    token: str = Depends(get_token),
    user_service: UserService = Depends(get_user_service),
) -> UserFullSchema:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token=token, key=auth_data["secret_key"], algorithms=auth_data["algorithm"]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return await user_service.get_user_by_id_full(int(user_id))


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role is UserRoles.ADMIN:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
