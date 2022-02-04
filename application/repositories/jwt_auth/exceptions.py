from fastapi import HTTPException


class Unauthorized(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Unauthorized",
        )
