from pydantic import BaseModel, EmailStr, Field, field_validator
from backend.app.tools.enums import CompleteStatus

class NoteCreateSchema(BaseModel):
    title: str = Field(..., max_length=128, detail='name of the task, max length = 128')
    content: str = Field(..., max_length=1024, 
                         detail='task content. max length = 1024')

class NoteUpdateSchema(BaseModel):
    pass

class NoteReadSchema(BaseModel):
    id: int
    title: str
    content: str
    status: CompleteStatus
    author_id: int
    book_id: int


    model_config = {'from_attributes': True}