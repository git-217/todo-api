from fastapi import APIRouter
from backend.app.api.endpoints.books import router as books_router
from backend.app.api.endpoints.users import router as users_router

api_router = APIRouter()

api_router.include_router(books_router)
api_router.include_router(users_router)