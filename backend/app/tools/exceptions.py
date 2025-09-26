from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Recourse not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "You don't have permission to access this resource"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict occurred"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AuthException(HTTPException):
    def __init__(self, detail: str = "Authorization error"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)