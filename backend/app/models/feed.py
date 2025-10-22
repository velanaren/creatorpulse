from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Feed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str               # e.g. "RSS", "YouTube", "Twitter"
    title: str
    link: str
    summary: Optional[str] = None
    published_at: datetime = Field(default_factory=datetime.utcnow)