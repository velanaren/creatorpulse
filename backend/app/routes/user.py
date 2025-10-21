from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.utils.database import get_session

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/")
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users