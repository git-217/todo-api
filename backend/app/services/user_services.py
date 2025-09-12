from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.user_repo import user_crud_repo
from backend.app.schemas.users_schema import UserRegisterSchema, UserUpdateSchema, UserGetSchema
from backend.app.models.users_models import User

class User:
    def __init__(self, db: AsyncSession):
        self.repo = user_crud_repo
        self.db = db

    async def create_user(self, user_data: UserRegisterSchema) -> User:
        user = await self.repo.create(db=self.db, obj_data = user_data.model_dump())
        return user

    async def delete_user_by_id(self, user_id: int) -> int:
        deleted_rowcount = await self.repo.delete(db=self.db, id=user_id)
        return deleted_rowcount

    async def change_user_data(self, user_id: int, new_data: UserUpdateSchema) -> int:
        changed_rowcounts = await self.repo.update(db=self.db,
                                                            filter_by={"id": user_id},
                                                            values=new_data.model_dump())
        return changed_rowcounts
        
    async def get_user_by_id(self, user_id: int) -> UserGetSchema | None:
        user = await self.repo.get(db=self.db, id=user_id)
        if user is None:
            return None
        try: 
            result = UserGetSchema.model_validate(user)
            return result
        except:
            print('no model dump :(')
            raise
            