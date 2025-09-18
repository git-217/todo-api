from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth_base import get_password_hash
from backend.app.db.repositories.user_repo import user_crud_repo
from backend.app.schemas.users_schema import (UserRegisterSchema, 
                                              UserUpdateSchema, 
                                              UserResponseSchema,
                                              UserAuthSchema)
from backend.app.db.models.users_models import User
from backend.app.core.auth_base import authenticate_user, create_access_token


class UserS:
    def __init__(self, db: AsyncSession):
        self.user_repo = user_crud_repo
        self.db = db

    async def create_user(self, user_data: UserRegisterSchema) -> User:
        user = await self.user_repo.create(db=self.db, obj_data = user_data.model_dump())
        return user

    async def delete_user_by_id(self, user_id: int) -> bool:
        return await self.user_repo.delete(db=self.db, id=user_id)

    async def change_user_data(self, *, user_id: int, new_data: UserUpdateSchema) -> int:
        changed_rowcounts = await self.user_repo.update(db=self.db,
                                                            filter_by={"id": user_id},
                                                            values=new_data.model_dump())
        return changed_rowcounts    

    async def get_user_or_none(self, **attrs):
        return await self.user_repo.get_one_or_none(db=self.db, **attrs)

    async def get_all_users(self):
        users = await self.user_repo.get_list(db=self.db)
        if users is None:
            return None
        return users

    async def get_user_by_id(self, user_id: int) -> UserResponseSchema | None:
        user = await self.user_repo.get(db=self.db, id=user_id)
        if user is None:
            return None
        return UserResponseSchema.model_validate(user)
    
    async def update(self, *, uid: int, user_data: UserUpdateSchema):
        upd = await self.user_repo.update(db=self.db, 
                                          id=uid, 
                                          new_data_obj=user_data)
        if not upd:
            return None
        return upd

    async def registrate_user(self, user_data: UserRegisterSchema):
        
        user = await self.user_repo.get_one_or_none(db=self.db, email = user_data.email)
        if user:
            return None
        user_data.password_hash = get_password_hash(user_data.password_hash)
        await self.user_repo.create(db=self.db, obj_data=user_data.model_dump())
        return True 


    async def create_access_token(self, user_data: UserAuthSchema) -> str | None:
        print('func create started')
        user = await authenticate_user(db=self.db, email=user_data.email, password=user_data.password)
        print('user is OK')
        if user is None:
            return None
        access_token = create_access_token({'sub': str(user.id)})
        return access_token
        


UserService = UserS