from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from ..database import Base

class Attendee(Base):
    __tablename__ = "attendees"

    attendee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20))
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    check_in_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)