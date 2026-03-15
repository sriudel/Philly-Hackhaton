from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()


@router.get("/artists")
async def match_artists_to_gig(
    gig_id: str = Query(..., description="Find artists that match this gig"),
    limit: int = Query(10, le=50),
):
    """
    Return top-N artists ranked by semantic similarity to the given gig.

    TODO: fetch gig embedding from Supabase (gigs.embedding)
    TODO: run pgvector cosine similarity query:
          SELECT *, embedding <=> $gig_embedding AS score
          FROM artist_profiles
          ORDER BY score
          LIMIT $limit
    TODO: return ranked list with match_score
    See: services/matching.py
    """
    return {
        "gig_id": gig_id,
        "matches": [],
        "message": "TODO: implement vector similarity search via pgvector",
    }


@router.get("/gigs")
async def match_gigs_to_artist(
    artist_id: str = Query(..., description="Find gigs that match this artist"),
    limit: int = Query(10, le=50),
):
    """
    Return top-N open gigs ranked by semantic similarity to the artist's profile.

    TODO: fetch artist embedding from Supabase (artist_profiles.embedding)
    TODO: run pgvector cosine similarity query:
          SELECT *, embedding <=> $artist_embedding AS score
          FROM gigs
          WHERE status = 'open'
          ORDER BY score
          LIMIT $limit
    TODO: return ranked list with match_score
    See: services/matching.py
    """
    return {
        "artist_id": artist_id,
        "matches": [],
        "message": "TODO: implement vector similarity search via pgvector",
    }


@router.post("/embed/gig/{gig_id}")
async def trigger_gig_embedding(gig_id: str):
    """
    Manually trigger embedding generation for a gig.
    Useful after bulk import or schema changes.
    TODO: fetch gig text, call OpenAI, store vector
    See: services/embeddings.py
    """
    return {"gig_id": gig_id, "message": "TODO: generate and store embedding"}


@router.post("/embed/artist/{user_id}")
async def trigger_artist_embedding(user_id: str):
    """
    Manually trigger embedding generation for an artist profile.
    TODO: fetch profile text, call OpenAI, store vector
    See: services/embeddings.py
    """
    return {"user_id": user_id, "message": "TODO: generate and store embedding"}
