from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class AttendeeBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    event_id: int
    check_in_status: bool = False

class AttendeeCreate(AttendeeBase):
    pass

class AttendeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    phone_number: Optional[str] = Field(None, max_length=20)
    check_in_status: Optional[bool]

class Attendee(AttendeeBase):
    attendee_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True