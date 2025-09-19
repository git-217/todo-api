from pydantic import BaseModel, EmailStr, Field, field_validator

class BookCreateSchema(BaseModel):
    title: str = Field(..., max_length=64, 
                       description='Title of the book, max 64 chars')
    description: str | None = Field(None, max_length=256, 
                                    description='Description of the book. Max 256 chars')



class BookUpdateSchema(BaseModel):
    pass

class BookResponseSchema(BaseModel):
    id: int
    title: str
    description: str | None

    model_config = {'from_attributes': True}