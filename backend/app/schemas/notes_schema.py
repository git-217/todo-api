from pydantic import BaseModel, EmailStr, Field, field_validator

class NoteCreateSchema(BaseModel):
    id: int

class NoteUpdateSchema(BaseModel):
    pass