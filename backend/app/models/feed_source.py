from sqlmodel import SQLModel, Field
from typing import Optional

class FeedSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str             # e.g. "AI", "Marketing"
    platform: str          # "RSS" | "YouTube"
    source_url: str        # RSS URL or YouTube channel ID
    active: bool = True