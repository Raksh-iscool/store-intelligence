from sqlalchemy.orm import Session

from app.models import Event


def get_health(db: Session):

    last_event = (
        db.query(Event)
        .order_by(Event.timestamp.desc())
        .first()
    )

    stores = (
        db.query(Event.store_id)
        .distinct()
        .count()
    )

    return {
        "status": "healthy",
        "stores": stores,
        "last_event_timestamp":
            last_event.timestamp if last_event else None,
        "stale_feed": False
    }