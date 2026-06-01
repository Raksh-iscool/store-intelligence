from sqlalchemy.orm import Session

from app.models import Event
from app.transaction_models import Transaction


def get_anomalies(
    db: Session,
    store_id: str
):

    anomalies = []

    queue_count = (
        db.query(Event)
        .filter(
            Event.store_id == store_id
        )
        .filter(
            Event.event_type ==
            "BILLING_QUEUE_JOIN"
        )
        .count()
    )

    if queue_count >= 5:
        anomalies.append({
            "severity": "WARN",
            "type": "QUEUE_SPIKE",
            "suggested_action":
            "Open additional billing counter"
        })

    visitors = (
        db.query(Event.visitor_id)
        .filter(
            Event.store_id == store_id
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

    conversion = 0

    if visitors:
        conversion = (
            purchases / visitors
        ) * 100

    if visitors > 0 and conversion < 20:
        anomalies.append({
            "severity": "WARN",
            "type": "CONVERSION_DROP",
            "suggested_action":
            "Investigate customer journey"
        })

    skincare_visits = (
        db.query(Event)
        .filter(
            Event.store_id == store_id
        )
        .filter(
            Event.zone_id == "SKINCARE"
        )
        .count()
    )

    if skincare_visits == 0:
        anomalies.append({
            "severity": "INFO",
            "type": "DEAD_ZONE",
            "suggested_action":
            "Review zone placement"
        })

    return anomalies