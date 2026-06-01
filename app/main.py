from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import get_db

from app.schemas import EventCreate

from app.ingestion import insert_event
from app.metrics import get_metrics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Store Intelligence API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/events/ingest")
def ingest_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):

    inserted = insert_event(
        db,
        event
    )

    return {
        "inserted": inserted
    }


@app.get("/stores/{store_id}/metrics")
def metrics(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_metrics(
        db,
        store_id
    )