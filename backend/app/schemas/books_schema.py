from pydantic import BaseModel

class BooksSchema(BaseModel):
    id: int

    