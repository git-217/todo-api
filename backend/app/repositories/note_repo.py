from backend.app.models.notes_models import Note
from backend.app.repositories.base_repo import CRUDBase
from backend.app.schemas.notes_schema import NoteCreateSchema, NoteUpdateSchema



class NoteCRUDRepo(CRUDBase[Note, NoteCreateSchema, NoteUpdateSchema]):
    ...

note_crud_repo = NoteCRUDRepo(Note)