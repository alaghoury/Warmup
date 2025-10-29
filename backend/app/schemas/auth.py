from pydantic import BaseModel

from .user import UserOut


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(TokenOut):
    user: UserOut
