from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Data to create a user (input)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    image: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None


# Data returned to the client (output — never exposes the password)
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    emailVerified: bool
    image: Optional[str]
    createdAt: datetime

    class Config:
        from_attributes = True  # Permite converter model SQLAlchemy → Pydantic


# Login schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# JWT token returned after login.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
