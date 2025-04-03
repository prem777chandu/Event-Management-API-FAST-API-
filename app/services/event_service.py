from datetime import datetime
from sqlalchemy.orm import Session
from ..models.event import Event as EventModel
from ..models.attendee import Attendee as AttendeeModel
from ..schemas.event import EventStatus

class EventService:
    @staticmethod
    def check_event_capacity(db: Session, event_id: int):
        event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
        if not event:
            return False, "Event not found"
        
        current_attendees = db.query(AttendeeModel).filter(
            AttendeeModel.event_id == event_id
        ).count()
        
        if current_attendees >= event.max_attendees:
            return False, "Event has reached maximum attendees"
        return True, ""

    @staticmethod
    def update_event_status(db: Session):
        now = datetime.utcnow()
        
        db.query(EventModel).filter(
            EventModel.start_time <= now,
            EventModel.end_time >= now,
            EventModel.status != EventStatus.canceled
        ).update({EventModel.status: EventStatus.ongoing})
        
        db.query(EventModel).filter(
            EventModel.end_time < now,
            EventModel.status.notin_([EventStatus.completed, EventStatus.canceled])
        ).update({EventModel.status: EventStatus.completed})
        
        db.commit()