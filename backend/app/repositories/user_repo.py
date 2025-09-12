from backend.app.schemas.users_schema import UserCreateSchema, UserUpdateSchema
from backend.app.models.users_models import User
from backend.app.repositories.base_repo import CRUDBase



class UserCRUDRepository(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    ...

user_crud_repo = UserCRUDRepository(User)