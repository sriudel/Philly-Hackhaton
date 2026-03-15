from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Gig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_id: str
    title: str
    category: str
    description: str
    pay: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    status: str = "open"          # open | filled | cancelled
    created_at: Optional[datetime] = None
    # embedding is stored in DB but not returned in API responses by default
