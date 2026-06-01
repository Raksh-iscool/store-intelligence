from sqlalchemy.orm import Session

from app.models import Event


def insert_event(db: Session, event):

    existing = (
        db.query(Event)
        .filter(Event.event_id == event.event_id)
        .first()
    )

    if existing:
        return False

    row = Event(**event.model_dump())

    db.add(row)

    db.commit()

    return True