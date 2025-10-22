import feedparser
from sqlmodel import Session
from datetime import datetime
from app.models.feed import Feed

def fetch_rss(url: str, session: Session, topic: str = "General"):
    """
    Fetches latest posts from an RSS feed and stores them in the database.
    """
    parsed = feedparser.parse(url)
    feeds = []

    for entry in parsed.entries[:10]:  # Limit to 10 recent items
        feed = Feed(
            source="RSS",
            title=entry.get("title", ""),
            link=entry.get("link", ""),
            summary=entry.get("summary", ""),
            published_at=datetime.utcnow(),
            topic=topic,  # 🔹 store topic name
        )
        session.add(feed)
        feeds.append(feed)

    session.commit()
    return feeds


def fetch_youtube(channel_id: str, session: Session, topic: str = "General"):
    """
    Fetches the latest 10 videos from a YouTube channel (using public RSS feed).
    """
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    parsed = feedparser.parse(url)
    feeds = []

    for entry in parsed.entries[:10]:
        feed = Feed(
            source="YouTube",
            title=entry.get("title", ""),
            link=entry.get("link", ""),
            summary=entry.get("summary", ""),
            published_at=datetime.utcnow(),
             topic=topic,  # 🔹 store topic name
        )
        session.add(feed)
        feeds.append(feed)

    session.commit()
    return feeds