from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ArtistProfile(BaseModel):
    user_id: str
    display_name: str
    bio: str
    category: str
    skills: List[str] = []
    location: Optional[str] = None
    portfolio_url: Optional[str] = None
    instagram_handle: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BusinessProfile(BaseModel):
    user_id: str
    business_name: str
    description: str
    industry: str
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
