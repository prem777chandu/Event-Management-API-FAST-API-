from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io

from ..database import get_db
from ..models.attendee import Attendee as AttendeeModel
from ..models.event import Event as EventModel
from ..schemas.attendee import Attendee, AttendeeCreate, AttendeeUpdate
from ..services.event_service import EventService
from ..utils.csv_processor import process_attendee_csv

router = APIRouter()

@router.post("/bulk-checkin", status_code=status.HTTP_201_CREATED)
async def bulk_check_in(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    
    contents = await file.read()
    csv_data = io.StringIO(contents.decode('utf-8'))
    reader = csv.DictReader(csv_data)
    
    results = process_attendee_csv(reader, event_id, db)
    
    return {
        "message": "Bulk check-in processed",
        "success_count": results["success_count"],
        "failed_count": results["failed_count"],
        "failed_entries": results["failed_entries"]
    }