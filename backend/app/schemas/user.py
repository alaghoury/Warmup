from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
