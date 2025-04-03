from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class EventStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

class EventBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: datetime
    end_time: datetime
    location: str = Field(..., max_length=100)
    max_attendees: int = Field(..., gt=0)
    status: EventStatus = EventStatus.scheduled

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str] = Field(None, max_length=100)
    max_attendees: Optional[int] = Field(None, gt=0)
    status: Optional[EventStatus]

class Event(EventBase):
    event_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True