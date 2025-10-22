from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Feed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str  # RSS or YouTube
    title: str
    link: str
    summary: Optional[str] = None
    topic: Optional[str] = None  # 🔹 new field
    published_at: datetime = Field(default_factory=datetime.utcnow)