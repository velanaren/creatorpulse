from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from typing import Optional
from app.utils.database import get_session
from app.models.feed import Feed
from app.models.feed_source import FeedSource
from app.services.fetcher import fetch_rss, fetch_youtube
from fastapi import HTTPException, Path


router = APIRouter(prefix="/api/feeds", tags=["feeds"])

@router.get("/")
def list_feeds(
    platform: Optional[str] = Query(None, description="Filter by platform: RSS or YouTube"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    q: Optional[str] = Query(None, description="Search keyword in title or summary"),
    limit: int = Query(10, description="Number of items to return"),
    session: Session = Depends(get_session)
):
    """
    List feeds with optional filters and sorting.
    Example: /api/feeds/?platform=RSS&topic=AI
    """
    query = select(Feed).order_by(Feed.published_at.desc())

    # Filter by platform (RSS / YouTube)
    if platform:
        query = query.where(Feed.source == platform)

    # Filter by topic
    if topic:
        subquery = select(FeedSource.platform).where(FeedSource.topic == topic)
        platforms = session.exec(subquery).all()
        if platforms:
            query = query.where(Feed.source.in_(platforms))

    # 🔍 Keyword search in title or summary
    if q:
        query = query.where(
            or_(
                Feed.title.ilike(f"%{q}%"),
                Feed.summary.ilike(f"%{q}%")
            )
        )

    results = session.exec(query.limit(limit)).all()
    return results

@router.post("/sync")
def manual_sync(session: Session = Depends(get_session)):
    """
    Manually trigger fetching for all active sources.
    """
    sources = session.exec(
        select(FeedSource).where(FeedSource.active == True)
    ).all()

    if not sources:
        return {"message": "No active sources found", "count": 0}

    total_feeds = 0
    for src in sources:
        try:
            if src.platform == "RSS":
                from app.utils.fetcher import fetch_rss
                feeds = fetch_rss(src.source_url, session, topic=src.topic)
                total_feeds += len(feeds)
            elif src.platform == "YouTube":
                from app.utils.fetcher import fetch_youtube
                feeds = fetch_youtube(src.source_url, session, topic=src.topic)
                total_feeds += len(feeds)
        except Exception as e:
            print(f"❌ Error syncing {src.source_url}: {e}")

    return {"message": "Sync completed", "count": total_feeds}

@router.get("/topics")
def get_topics(session: Session = Depends(get_session)):
    """
    Fetch unique topics from the FeedSource table.
    Returns only active ones.
    """
    results = session.exec(
        select(FeedSource.topic)
        .where(FeedSource.active == True)
        .distinct()
    ).all()
    # Filter out None or empty topics
    topics = [t for t in results if t]
    return {"topics": topics}

from fastapi import HTTPException
from app.models import FeedSource

@router.post("/sources")
def add_source(
    platform: str = Query(..., description="Platform: RSS or YouTube"),
    topic: str = Query(..., description="Topic for this source"),
    source_url: str = Query(..., description="Feed URL or Channel ID"),
    session: Session = Depends(get_session)
):
    """
    Add a new content source for automatic fetching.
    Example:
    POST /api/sources?platform=RSS&topic=AI&source_url=https://rss.nytimes.com/ai.xml
    """
    # 🧩 Prevent duplicates
    existing = session.exec(
        select(FeedSource).where(
            FeedSource.source_url == source_url, FeedSource.topic == topic
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source already exists")

    new_source = FeedSource(
        platform=platform,
        topic=topic,
        source_url=source_url,
        active=True,
    )
    session.add(new_source)
    session.commit()
    session.refresh(new_source)
    return {"message": "Source added successfully", "source": new_source}

@router.get("/sources")
def list_sources(session: Session = Depends(get_session)):
    """
    Get all FeedSources with their status.
    """
    sources = session.exec(select(FeedSource)).all()
    return sources

# ✅ Toggle active/inactive source
@router.patch("/source/{source_id}/toggle")
def toggle_source(
    source_id: int = Path(..., description="ID of the source to toggle"),
    session: Session = Depends(get_session)
):
    source = session.get(FeedSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source.active = not source.active
    session.add(source)
    session.commit()
    session.refresh(source)
    return {"message": "Source toggled", "active": source.active}


# ✅ Delete a source
@router.delete("/source/{source_id}")
def delete_source(
    source_id: int = Path(..., description="ID of the source to delete"),
    session: Session = Depends(get_session)
):
    source = session.get(FeedSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    session.delete(source)
    session.commit()
    return {"message": "Source deleted successfully"}

@router.post("/rss")
def fetch_rss_feed(
    url: str = Query(..., description="RSS feed URL"),
    session: Session = Depends(get_session),
    topic: Optional[str] = "General"
):
    feeds = fetch_rss(url, session, topic)
    return {"status": "success", "items_added": len(feeds)}


@router.post("/youtube")
def fetch_youtube_feed(
    channel_id: str = Query(..., description="YouTube channel ID"),
    session: Session = Depends(get_session),
    topic: Optional[str] = "General"
):
    feeds = fetch_youtube(channel_id, session, topic)
    return {"status": "success", "items_added": len(feeds)}