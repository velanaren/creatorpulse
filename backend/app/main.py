from fastapi import FastAPI
from app.routes import base
from app.utils.database import init_db
from app.routes import user as user_routes
from app.models import user, feed, feed_source
from app.routes import feed
from app.services.auto_fetcher import start_scheduler
start_scheduler()

from app.routes import feed_source



app = FastAPI(title="CreatorPulse API", version="0.1")

# include base routes
app.include_router(base.router)
app.include_router(user_routes.router)
app.include_router(feed.router)
app.include_router(feed_source.router)


@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.utils.database import init_db

@app.on_event("startup")
def on_startup():
    init_db()