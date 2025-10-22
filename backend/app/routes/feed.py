from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import Optional
from app.utils.database import get_session
from app.models.feed import Feed
from app.models.feed_source import FeedSource
from app.services.fetcher import fetch_rss, fetch_youtube

router = APIRouter(prefix="/api/feeds", tags=["feeds"])

@router.get("/")
def list_feeds(
    platform: Optional[str] = Query(None, description="Filter by platform: RSS or YouTube"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    limit: int = Query(10, description="Number of items to return"),
    session: Session = Depends(get_session)
):
    """
    List feeds with optional filters and sorting.
    Example: /api/feeds/?platform=RSS&topic=AI
    """
    query = select(Feed).order_by(Feed.published_at.desc())

    if platform:
        query = query.where(Feed.source == platform)

    # TEMP: ignore URL matching and just filter by topic’s platform
    if topic:
        subquery = select(FeedSource.platform).where(FeedSource.topic == topic)
        platforms = session.exec(subquery).all()
        if platforms:
            query = query.where(Feed.source.in_(platforms))

    results = session.exec(query.limit(limit)).all()
    return results

@router.post("/rss")
def fetch_rss_feed(
    url: str = Query(..., description="RSS feed URL"),
    session: Session = Depends(get_session),
):
    feeds = fetch_rss(url, session)
    return {"status": "success", "items_added": len(feeds)}


@router.post("/youtube")
def fetch_youtube_feed(
    channel_id: str = Query(..., description="YouTube channel ID"),
    session: Session = Depends(get_session),
):
    feeds = fetch_youtube(channel_id, session)
    return {"status": "success", "items_added": len(feeds)}