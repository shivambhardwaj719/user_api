from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class StaffCreate(BaseModel):
    person_name: str
    gender: str
    phone_number: str
    official_email_id: Optional[EmailStr] = None
    personal_email_id: EmailStr
    staff_type: str
    create_user: bool = False

class StaffUpdate(BaseModel):
    person_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_enabled: Optional[bool] = None

class StaffResponse(BaseModel):
    id: int
    person_name: str
    gender: str
    phone_number: str
    staff_type: str
    is_enabled: bool

    class Config:
        from_attributes = True

class StaffActionRequest(BaseModel):
    action: str  # 'enable' or 'disable'
