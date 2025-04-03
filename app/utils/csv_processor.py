from sqlalchemy.orm import Session
from ..models.attendee import Attendee as AttendeeModel

def process_attendee_csv(reader, event_id: int, db: Session):
    success_count = 0
    failed_count = 0
    failed_entries = []
    
    for row in reader:
        try:
            attendee = db.query(AttendeeModel).filter(
                AttendeeModel.email == row['email'],
                AttendeeModel.event_id == event_id
            ).first()
            
            if attendee and not attendee.check_in_status:
                attendee.check_in_status = True
                db.commit()
                success_count += 1
            else:
                failed_count += 1
                failed_entries.append({
                    'email': row['email'],
                    'reason': 'Already checked in or not registered'
                })
        except Exception as e:
            failed_count += 1
            failed_entries.append({
                'email': row.get('email', ''),
                'reason': str(e)
            })
    
    return {
        "success_count": success_count,
        "failed_count": failed_count,
        "failed_entries": failed_entries
    }