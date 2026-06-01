from sqlalchemy.orm import Session
from app.models import Event

def insert_events(db: Session, events):

    inserted = 0
    duplicates = 0

    for event in events:

        existing = (
            db.query(Event)
            .filter(Event.event_id == event.event_id)
            .first()
        )

        if existing:
            duplicates += 1
            continue

        row = Event(**event.model_dump())
        db.add(row)
        inserted += 1

    db.commit()

    return {
        "inserted": inserted,
        "duplicates": duplicates
    }