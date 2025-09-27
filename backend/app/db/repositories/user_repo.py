from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.schemas.users_schema import UserCreateSchema, UserUpdateSchema
from app.db.models.users_models import User
from app.db.repositories.base_repo import CRUDBase


class UserCRUDRepo(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    async def get_one_or_none(self, *, db: AsyncSession, **search_keys) -> User | None:
        query = select(self.model).filter_by(**search_keys)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_or_none(
        self,
        *,
        db: AsyncSession,
        id: int,
        include_books: bool = False,
        include_notes: bool = False,
    ) -> User | None:

        query = select(self.model).where(self.model.id == id)
        if include_books:
            query = query.options(selectinload(self.model.books))
        if include_notes:
            query = query.options(selectinload(self.model.notes))
        result = await db.execute(query)
        return result.scalar_one_or_none()


user_crud_repo = UserCRUDRepo(User)
