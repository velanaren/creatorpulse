from sqlmodel import SQLModel, create_engine
from app.models.feed import Feed
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)