from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    email: EmailStr
    password: str
    phone: str

class UserResponse(BaseModel):
    first_name: str
    email: EmailStr
    phone: str
    profile_picture: Optional[str] = None
    message: Optional[str] = None