from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.notes_models import Note
from app.db.repositories.base_repo import CRUDBase
from app.schemas.notes_schema import NoteCreateSchema, NoteUpdateSchema



class NoteCRUDRepo(CRUDBase[Note, NoteCreateSchema, NoteUpdateSchema]):
    ...

note_crud_repo = NoteCRUDRepo(Note)