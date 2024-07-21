from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    profile_picture: Optional[bytes] = None

class UserResponse(BaseModel):
    first_name: str
    email: EmailStr
    phone: str
    profile_picture: Optional[str] = None

class MessageResponse(BaseModel):
    message: str