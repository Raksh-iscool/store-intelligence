from typing import Optional

from pydantic import BaseModel

from typing import List



class EventCreate(BaseModel):
    event_id: str
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: str

    zone_id: Optional[str] = None

    dwell_ms: int = 0

    is_staff: bool = False

    confidence: float = 0.0


class EventResponse(EventCreate):
    pass

class EventBatch(BaseModel):
    events: List[EventCreate]