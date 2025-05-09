from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class EventBaseModel(BaseModel):
    id: Optional[str]
    name: str
    description: str
    location: str
    available_tickets: int
    price: float
    image: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class OrderSchema(BaseModel):
    event_id: str
    event_name: str
    quantity: int
    price: float
    total_price: float
    order_time: datetime