from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.users_schema import UserCreateSchema, UserUpdateSchema
from backend.app.db.models.users_models import User
from backend.app.db.repositories.base_repo import CRUDBase



class UserCRUDRepository(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    async def get_one_or_none(self, *, db: AsyncSession, **search_keys):
        print(f'search_keys: {search_keys}')
        query = select(self.model).filter_by(**search_keys)
        result = await db.execute(query)
        return result.scalar_one_or_none()

user_crud_repo = UserCRUDRepository(User)