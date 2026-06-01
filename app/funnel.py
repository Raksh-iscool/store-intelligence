from sqlalchemy.orm import Session

from app.models import Event
from app.transaction_models import Transaction


def get_funnel(
    db: Session,
    store_id: str
):

    entry_visitors = set(
        row.visitor_id
        for row in db.query(Event)
        .filter(Event.store_id == store_id)
        .filter(Event.event_type == "ENTRY")
        .all()
    )

    zone_visitors = set(
        row.visitor_id
        for row in db.query(Event)
        .filter(Event.store_id == store_id)
        .filter(Event.event_type.in_([
            "ZONE_ENTER",
            "ZONE_DWELL"
        ]))
        .all()
    )

    queue_visitors = set(
        row.visitor_id
        for row in db.query(Event)
        .filter(Event.store_id == store_id)
        .filter(
            Event.event_type ==
            "BILLING_QUEUE_JOIN"
        )
        .all()
    )

    purchases = (
        db.query(Transaction)
        .filter(
            Transaction.store_id == store_id
        )
        .count()
    )

    entry = len(entry_visitors)
    zone = len(zone_visitors)
    queue = len(queue_visitors)

    drop_zone = 0
    drop_queue = 0
    drop_purchase = 0

    if entry:
        drop_zone = round(
            ((entry - zone) / entry) * 100,
            2
        )

    if zone:
        drop_queue = round(
            ((zone - queue) / zone) * 100,
            2
        )

    if queue:
        drop_purchase = round(
            ((queue - purchases) / queue) * 100,
            2
        )

    return {
        "entry": entry,
        "zone_visit": zone,
        "billing_queue": queue,
        "purchase": purchases,
        "dropoff_zone": drop_zone,
        "dropoff_queue": drop_queue,
        "dropoff_purchase": drop_purchase
    }