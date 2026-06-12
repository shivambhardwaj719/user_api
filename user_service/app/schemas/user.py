from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    gender: str
    account_type: Optional[str] = "sub_admin"
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    is_enabled: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: str
    gender: str
    account_type: str
    is_enabled: bool
    is_active: bool

    class Config:
        from_attributes = True

class UserStatusAction(BaseModel):
    action: str
