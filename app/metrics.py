from sqlalchemy.orm import Session

from app.models import Event
from app.transaction_models import Transaction


def get_metrics(
    db: Session,
    store_id: str
):

    visitors = (
        db.query(Event.visitor_id)
        .filter(
            Event.store_id == store_id
        )
        .filter(
            Event.is_staff == False
        )
        .distinct()
        .count()
    )

    purchases = (
        db.query(Transaction)
        .filter(
            Transaction.store_id == store_id
        )
        .count()
    )

    conversion_rate = 0

    if visitors > 0:
        conversion_rate = (
            purchases / visitors
        ) * 100

    dwell_events = (
        db.query(Event)
        .filter(
            Event.store_id == store_id
        )
        .filter(
            Event.dwell_ms > 0
        )
        .all()
    )

    avg_dwell = 0

    if dwell_events:
        avg_dwell = (
            sum(
                e.dwell_ms
                for e in dwell_events
            )
            / len(dwell_events)
        )

    return {
        "unique_visitors": visitors,
        "purchases": purchases,
        "conversion_rate": round(
            conversion_rate,
            2
        ),
        "average_dwell_ms": round(
            avg_dwell,
            2
        )
    }