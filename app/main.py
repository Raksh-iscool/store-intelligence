from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import get_db

from app.schemas import EventCreate


from app.metrics import get_metrics
from app.schemas import EventBatch
from app.ingestion import insert_events

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
def ingest_events(
    payload: EventBatch,
    db: Session = Depends(get_db)
):
    result = insert_events(
        db,
        payload.events
    )

    return {
        "received": len(payload.events),
        **result
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