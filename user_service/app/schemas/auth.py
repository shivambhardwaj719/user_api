from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access: str
    refresh: str


class SetMPinRequest(BaseModel):
    mpin: int

class CheckMPinRequest(BaseModel):
    mpin: int

class VerifyPasswordRequest(BaseModel):
    password: str
