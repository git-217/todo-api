import re
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserSchema(BaseModel):
    id: int
    
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name. Min=1, max=50")
    last_name: str | None = Field(None, min_length=1, max_length=50, description="User's last name. Min=1, max=50")
    email: EmailStr = Field(..., description="User's email")
    phone_number: str = Field(..., description="User's phone number. 1-15 nums, '+x' format)")

    book_id: int | None = Field(None, description="User's book")


    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Phone number must begins with "+" and contains 1 to 15 nums')
        return value
    