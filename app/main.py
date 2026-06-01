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
from app.transaction_models import Transaction
from app.transactions import create_transaction
from app.funnel import get_funnel
from app.heatmap import get_heatmap


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

@app.post("/transactions/demo")
def add_demo_transaction(
    db: Session = Depends(get_db)
):

    create_transaction(
        db,
        transaction_id="TXN_001",
        store_id="STORE_BLR_001",
        timestamp="2026-03-03T14:30:00Z",
        basket_value=1200
    )

    return {
        "message": "transaction added"
    }
@app.get("/stores/{store_id}/funnel")
def funnel(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_funnel(
        db,
        store_id
    )

@app.get("/stores/{store_id}/heatmap")
def heatmap(
    store_id: str,
    db: Session = Depends(get_db)
):
    return get_heatmap(
        db,
        store_id
    )