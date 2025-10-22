from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.utils.database import get_session
from app.models.feed_source import FeedSource

router = APIRouter(prefix="/api/sources", tags=["feed_sources"])

@router.post("/")
def add_source(source: FeedSource, session: Session = Depends(get_session)):
    session.add(source)
    session.commit()
    session.refresh(source)
    return source

@router.get("/")
def list_sources(session: Session = Depends(get_session)):
    return session.exec(select(FeedSource)).all()

@router.put("/{source_id}")
def toggle_source(source_id: int, session: Session = Depends(get_session)):
    source = session.get(FeedSource, source_id)
    if not source:
        return {"error": "Source not found"}
    source.active = not source.active
    session.add(source)
    session.commit()
    return {"id": source.id, "active": source.active}