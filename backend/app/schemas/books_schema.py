from pydantic import BaseModel, Field
from backend.app.tools.enums import CompleteStatus

class BookCreateSchema(BaseModel):
    title: str = Field(..., 
                       max_length=64, 
                       description='Title of the book, max 64 chars')
    description: str | None = Field(None, 
                                    max_length=256, 
                                    description='Description of the book. Max 256 chars')



class BookUpdateSchema(BaseModel):
    id: int
    title: str | None = Field(None, 
                              max_length=64, 
                              description='Title of the book, max 64 chars')
    description: str | None = Field(None, 
                                    max_length=256, 
                                    description='Description of the book. Max 256 chars')


class BookReadSchema(BaseModel):
    id: int
    title: str
    description: str | None
    status: CompleteStatus

    model_config = {'from_attributes': True}