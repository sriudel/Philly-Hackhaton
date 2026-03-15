from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()


class GigCreate(BaseModel):
    title: str
    category: str
    description: str
    pay: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    # business_id will come from auth middleware once implemented


class GigResponse(BaseModel):
    id: str
    title: str
    category: str
    description: str
    pay: Optional[str]
    date: Optional[str]
    location: Optional[str]
    status: str
    business_id: str


@router.get("/")
async def list_gigs(business_id: Optional[str] = None, category: Optional[str] = None):
    """
    List gigs. Optionally filter by business or category.
    TODO: query Supabase gigs table
    TODO: add pagination (limit/offset)
    """
    return {"gigs": [], "message": "TODO: fetch from Supabase"}


@router.get("/{gig_id}")
async def get_gig(gig_id: str):
    """
    TODO: fetch single gig by ID from Supabase
    TODO: also return applicant count
    """
    return {"gig_id": gig_id, "message": "TODO: fetch from Supabase"}


@router.post("/", status_code=201)
async def create_gig(body: GigCreate):
    """
    Create a new gig and generate its embedding for matching.
    TODO: verify user is authenticated and has role=business
    TODO: insert into gigs table
    TODO: call services/embeddings.py to generate embedding from title+description
    TODO: store embedding in gigs.embedding column (pgvector)
    """
    fake_id = str(uuid.uuid4())
    return {"id": fake_id, **body.model_dump(), "status": "open", "message": "TODO: persist to Supabase"}


@router.patch("/{gig_id}")
async def update_gig(gig_id: str, body: dict):
    """
    TODO: verify requester owns this gig
    TODO: update gig fields in Supabase
    TODO: re-embed if title/description changed
    """
    return {"gig_id": gig_id, "message": "TODO: update in Supabase"}


@router.delete("/{gig_id}", status_code=204)
async def delete_gig(gig_id: str):
    """
    TODO: soft delete (set status='deleted') rather than hard delete
    TODO: verify requester owns this gig
    """
    return
