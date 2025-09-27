from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypt import get_password_hash
from app.db.repositories.user_repo import user_crud_repo
from app.schemas.users_schema import (
    UserRegisterSchema,
    UserUpdateSchema,
    UserBasicSchema,
    UserWithBooksSchema,
    UserWithNotesSchema,
    UserAuthSchema,
    UserFullSchema,
)
from app.core.crypt import authenticate_user, create_access_token
from app.tools.exceptions import NotFoundException


class UserService:
    def __init__(self, db: AsyncSession, user_repo=user_crud_repo):
        self.user_repo = user_repo
        self.db = db

    async def create_user(self, user_data: UserRegisterSchema) -> UserBasicSchema:
        user = await self.user_repo.create(db=self.db, obj_data=user_data)
        return UserBasicSchema.model_validate(user)

    async def change_user_data(
        self, *, user_id: int, new_data: UserUpdateSchema
    ) -> UserBasicSchema:
        new_user = await self.user_repo.update(
            db=self.db, filter_by={"id": user_id}, values=new_data.model_dump()
        )
        return UserBasicSchema.model_validate(new_user)

    async def get_all_users(self) -> list[UserBasicSchema]:
        users = await self.user_repo.get_list(db=self.db)
        if users is None:
            raise NotFoundException("There's no users")

        users_schemas = [UserBasicSchema.model_validate(b) for b in users]
        return users_schemas

    async def get_user_by_id_basic(self, user_id: int) -> UserBasicSchema:
        user = await self.user_repo.get_by_id_or_none(
            db=self.db,
            id=user_id,
        )
        if user is None:
            raise NotFoundException("User doesn't exist")
        return UserBasicSchema.model_validate(user)

    async def get_user_by_id_with_books(self, user_id: int) -> UserWithBooksSchema:
        user = await self.user_repo.get_by_id_or_none(
            db=self.db, id=user_id, include_books=True
        )
        if user is None:
            raise NotFoundException("User doesn't exist")
        user.book_ids = [b.id for b in user.books] if user.books else []
        return UserWithBooksSchema.model_validate(user)

    async def get_user_by_id_with_notes(self, user_id: int) -> UserWithNotesSchema:
        user = await self.user_repo.get_by_id_or_none(
            db=self.db, id=user_id, include_notes=True
        )
        if user is None:
            raise NotFoundException("User doesn't exist")
        user.note_ids = [n.id for n in user.notes] if user.notes else []
        return UserWithNotesSchema.model_validate(user)

    async def get_user_by_id_full(self, user_id: int) -> UserFullSchema:
        user = await self.user_repo.get_one_or_none(db=self.db, id=user_id)
        if user is None:
            raise NotFoundException("User doesn't exist")

        user = await self.user_repo.get_by_id_or_none(
            db=self.db, id=user_id, include_books=True, include_notes=True
        )
        if user is None:
            raise NotFoundException("User doesn't exist")
        user.book_ids = [b.id for b in user.books] if user.books else []
        user.note_ids = [n.id for n in user.notes] if user.notes else []
        schema = UserFullSchema.model_validate(user)
        return schema

    async def delete_user_by_id(self, user_id: int) -> UserBasicSchema:
        user = await self.user_repo.get_by_id_or_none(
            db=self.db, id=user_id, include_books=True, include_notes=True
        )

        deleted_user = await self.user_repo.delete(db=self.db, id=user_id)

        if deleted_user is None:
            raise NotFoundException("User doesn't exist")

        return UserBasicSchema.model_validate(deleted_user)

    async def update(self, *, uid: int, user_data: UserUpdateSchema) -> UserBasicSchema:
        updated_user = await self.user_repo.update(
            db=self.db, id=uid, new_data_obj=user_data
        )
        return UserBasicSchema.model_validate(updated_user)

    async def registrate_user(self, user_data: UserRegisterSchema) -> UserBasicSchema:

        user = await self.user_repo.get_one_or_none(db=self.db, email=user_data.email)
        if user:
            raise NotFoundException("User already exists")
        user_data.password_hash = get_password_hash(user_data.password_hash)
        new_user = await self.user_repo.create(db=self.db, obj_data=user_data)
        return UserBasicSchema.model_validate(new_user)

    async def create_access_token(self, user_data: UserAuthSchema) -> dict:
        user = await authenticate_user(
            db=self.db, email=user_data.email, password=user_data.password
        )
        if user is None:
            raise NotFoundException("User with that email doesn't exist")
        access_token = create_access_token({"sub": str(user.id)})
        return access_token
