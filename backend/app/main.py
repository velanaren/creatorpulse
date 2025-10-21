from fastapi import FastAPI
from app.routes import base
from app.utils.database import init_db
from app.routes import user

app = FastAPI(title="CreatorPulse API", version="0.1")

# include base routes
app.include_router(base.router)
app.include_router(user.router)

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