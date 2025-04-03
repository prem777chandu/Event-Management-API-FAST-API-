from fastapi import FastAPI, Depends
from .database import engine, Base
from app.routers import event, attendee, auth
from .services.event_service import EventService
from .dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management API",
    description="API for managing events and attendees with JWT authentication",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(
    event.router,
    prefix="/api/v1/events",
    tags=["events"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    attendee.router,
    prefix="/api/v1/attendees",
    tags=["attendees"],
    dependencies=[Depends(get_current_user)]
)

@app.on_event("startup")
async def startup_event():
    
    from .database import SessionLocal
    db = SessionLocal()
    EventService.update_event_status(db)
    db.close()

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Event Management API is running"}