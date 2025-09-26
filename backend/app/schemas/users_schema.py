import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from app.tools.enums import UserRoles

class BaseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    role: UserRoles 

    model_config = ConfigDict(from_attributes=True)
    
class UserBasicSchema(BaseSchema):
    pass

class UserWithBooksSchema(BaseSchema):
    book_ids: list[int] = []

class UserWithNotesSchema(BaseSchema):
    note_ids: list[int] = []

class UserFullSchema(BaseSchema):
    book_ids: list[int] = []
    note_ids: list[int] = []

class UserCreateSchema(BaseModel):
    id: int

class UserUpdateSchema(BaseModel):
    pass


class UserRegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, 
                                 description="User's first name. Min=1, max=50")
    last_name: str | None = Field(None, min_length=1, max_length=50, 
                                 description="User's last name. Min=1, max=50")
    email: EmailStr = Field(..., description="User's email")
    password_hash: str = Field(..., min_length=8, max_length=50, 
                                 description="User's password. Min=8, max=50, atleast must contain 1 special character")

    @field_validator('password_hash')
    @classmethod
    def validate_password(cls, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain atleast 1 special character')
        return value


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(..., description='Email')
    password: str = Field(..., description='Password')

class PatchUserNamesSchema(BaseModel):
    first_name: str = Field(..., description="User's name")
    last_name: str | None = Field(None, description="User's last name")