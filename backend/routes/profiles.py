from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class ArtistProfileUpsert(BaseModel):
    display_name: str
    bio: str
    category: str          # e.g. "Jazz Musician", "Muralist"
    skills: List[str]      # e.g. ["piano", "improvisation"]
    location: Optional[str] = None
    portfolio_url: Optional[str] = None
    instagram_handle: Optional[str] = None


class BusinessProfileUpsert(BaseModel):
    business_name: str
    description: str
    industry: str
    location: Optional[str] = None
    website: Optional[str] = None


@router.get("/artist/{user_id}")
async def get_artist_profile(user_id: str):
    """
    TODO: fetch artist_profiles row for user_id from Supabase
    """
    return {"user_id": user_id, "message": "TODO: fetch from Supabase"}


@router.put("/artist/{user_id}")
async def upsert_artist_profile(user_id: str, body: ArtistProfileUpsert):
    """
    Create or update an artist profile.
    TODO: upsert into artist_profiles table
    TODO: re-generate embedding from bio+skills+category
    TODO: store embedding in artist_profiles.embedding (pgvector)
    """
    return {"user_id": user_id, **body.model_dump(), "message": "TODO: persist to Supabase"}


@router.get("/business/{user_id}")
async def get_business_profile(user_id: str):
    """
    TODO: fetch business_profiles row for user_id from Supabase
    """
    return {"user_id": user_id, "message": "TODO: fetch from Supabase"}


@router.put("/business/{user_id}")
async def upsert_business_profile(user_id: str, body: BusinessProfileUpsert):
    """
    Create or update a business profile.
    TODO: upsert into business_profiles table
    TODO: re-generate embedding from description+industry
    """
    return {"user_id": user_id, **body.model_dump(), "message": "TODO: persist to Supabase"}
