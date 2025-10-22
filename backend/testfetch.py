from sqlmodel import Session
from app.services.fetcher import fetch_rss
from app.utils.database import engine

url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"

with Session(engine) as session:
    feeds = fetch_rss(url, session)
    print(f"{len(feeds)} items saved.")