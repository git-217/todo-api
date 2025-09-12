from pydantic import BaseModel, EmailStr, Field, field_validator

class BookCreateSchema(BaseModel):
    id: int

class BookUpdateSchema(BaseModel):
    pass

class BookResponseSchema(BaseModel):
    title: str
    description: str | None