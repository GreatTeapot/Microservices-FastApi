import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, validator, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator('password')
    def password_must_contain_letter_and_digit(cls, value):
        if not re.search(r'[A-Za-z]', value):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one digit')
        return value


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    role: str

    class Config:
        from_attributes = True


class SuperUser(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=2, max_length=30)]
    role : str
    is_superuser: bool = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str