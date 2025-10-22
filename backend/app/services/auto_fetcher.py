from sqlmodel import Session, select
from app.utils.database import engine
from app.models.feed_source import FeedSource
from app.services.fetcher import fetch_rss, fetch_youtube
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def run_auto_fetch():
    """
    Fetch all active FeedSources every few hours automatically.
    """
    print(f"[{datetime.utcnow()}] ⏳ Auto-fetch job started")
    with Session(engine) as session:
        sources = session.exec(select(FeedSource).where(FeedSource.active == True)).all()
        for src in sources:
            print(f"Fetching from: {src.platform} | {src.topic} | {src.source_url}")
            if src.platform.lower() == "rss":
                fetch_rss(src.source_url, session, topic=src.topic or "General")
            elif src.platform.lower() == "youtube":
                fetch_youtube(src.source_url, session, topic=src.topic or "General")

    print(f"[{datetime.utcnow()}] ✅ Auto-fetch job completed")


def start_scheduler():
    """
    Start APScheduler background job to refresh feeds every 6 hours.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_auto_fetch, "interval", hours=6)
    scheduler.start()
    print("🕓 Scheduler started — will auto-fetch feeds every 6 hours.")