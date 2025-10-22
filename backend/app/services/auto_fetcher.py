from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session, select
from app.utils.database import engine
from app.models.feed_source import FeedSource
from app.services.fetcher import fetch_rss, fetch_youtube

def run_auto_fetch():
    with Session(engine) as session:
        sources = session.exec(select(FeedSource).where(FeedSource.active == True)).all()
        for src in sources:
            if src.platform.lower() == "rss":
                fetch_rss(src.source_url, session)
            elif src.platform.lower() == "youtube":
                fetch_youtube(src.source_url, session)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_auto_fetch, "interval", hours=6)
    scheduler.start()