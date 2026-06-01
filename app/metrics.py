from sqlalchemy.orm import Session

from app.models import Event


def get_metrics(db: Session, store_id: str):

    visitors = (
        db.query(Event.visitor_id)
        .filter(Event.store_id == store_id)
        .filter(Event.is_staff == False)
        .distinct()
        .count()
    )

    avg_dwell = (
        db.query(Event)
        .filter(Event.store_id == store_id)
        .filter(Event.dwell_ms > 0)
        .all()
    )

    dwell = 0

    if avg_dwell:
        dwell = sum(x.dwell_ms for x in avg_dwell) / len(avg_dwell)

    return {
        "unique_visitors": visitors,
        "average_dwell_ms": round(dwell, 2)
    }