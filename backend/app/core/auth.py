from passlib.context import CryptContext

from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from backend.app.core.config import get_auth_data
from backend.app.db.repositories.user_repo import user_crud_repo

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({'exp': expire})

    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await user_crud_repo.get_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password_hash) is False:
        return None
    return user