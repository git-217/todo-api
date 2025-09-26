from fastapi import APIRouter
from app.api.endpoints.books import router as books_router
from app.api.endpoints.users import router as users_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.notes import router as note_router

api_router = APIRouter()

api_router.include_router(books_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(note_router)