from fastapi import APIRouter
from backend.app.schemas.books_schema import BookCreateSchema


router = APIRouter(prefix='/books')

