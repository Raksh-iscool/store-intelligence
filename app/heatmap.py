from collections import defaultdict

from sqlalchemy.orm import Session

from app.models import Event


def get_heatmap(
    db: Session,
    store_id: str
):

    zone_visits = defaultdict(int)
    zone_dwell = defaultdict(list)

    events = (
        db.query(Event)
        .filter(Event.store_id == store_id)
        .all()
    )

    sessions = set()

    for event in events:

        sessions.add(event.visitor_id)

        if not event.zone_id:
            continue

        zone_visits[event.zone_id] += 1

        if event.dwell_ms > 0:
            zone_dwell[event.zone_id].append(
                event.dwell_ms
            )

    max_visits = max(
        zone_visits.values(),
        default=1
    )

    result = []

    for zone in zone_visits:

        avg_dwell = 0

        if zone_dwell[zone]:
            avg_dwell = (
                sum(zone_dwell[zone])
                / len(zone_dwell[zone])
            )

        score = round(
            (zone_visits[zone] / max_visits)
            * 100,
            2
        )

        result.append({
            "zone": zone,
            "visits": zone_visits[zone],
            "avg_dwell": round(avg_dwell, 2),
            "score": score
        })

    confidence = "LOW"

    if len(sessions) >= 20:
        confidence = "HIGH"

    return {
        "zones": result,
        "data_confidence": confidence
    }