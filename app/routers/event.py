from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.event import Event as EventModel
from ..schemas.event import Event, EventCreate, EventUpdate, EventStatus

router = APIRouter()


@router.get("/events/")
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(EventModel).offset(skip).limit(limit).all()

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    if event.start_time >= event.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    db_event = EventModel(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event.model_dump(exclude_unset=True)
    
    if 'start_time' in update_data or 'end_time' in update_data:
        start_time = update_data.get('start_time', db_event.start_time)
        end_time = update_data.get('end_time', db_event.end_time)
        if start_time >= end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )
    
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[Event])
def list_events(
    status: Optional[EventStatus] = None,
    location: Optional[str] = None,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EventModel)
    
    if status:
        query = query.filter(EventModel.status == status)
    if location:
        query = query.filter(EventModel.location.ilike(f"%{location}%"))
    if date:
        query = query.filter(
            (EventModel.start_time <= date) & (EventModel.end_time >= date)
        )
    
    return query.order_by(EventModel.start_time).all()

@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event