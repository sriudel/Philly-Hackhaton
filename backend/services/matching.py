"""
Matching service — cosine similarity via pgvector.

pgvector operators:
  <=>  cosine distance   (lower = more similar; 0 = identical)
  <->  L2 (Euclidean) distance
  <#>  inner product (negative)

We use <=> and return (1 - distance) as the match_score (0–1).
"""

from db.client import get_supabase


async def top_artists_for_gig(gig_embedding: list[float], limit: int = 10) -> list[dict]:
    """
    Query artist_profiles ordered by cosine similarity to the gig embedding.

    TODO: run this query via Supabase RPC or raw postgres:

        SELECT
            ap.*,
            1 - (ap.embedding <=> $1::vector) AS match_score
        FROM artist_profiles ap
        ORDER BY ap.embedding <=> $1::vector
        LIMIT $2;

    For Supabase, create a Postgres function and call it via:
        supabase.rpc("match_artists", {"query_embedding": gig_embedding, "match_count": limit})
    """
    # TODO: implement with Supabase RPC
    return []


async def top_gigs_for_artist(artist_embedding: list[float], limit: int = 10) -> list[dict]:
    """
    Query open gigs ordered by cosine similarity to the artist embedding.

    TODO: run this query via Supabase RPC or raw postgres:

        SELECT
            g.*,
            1 - (g.embedding <=> $1::vector) AS match_score
        FROM gigs g
        WHERE g.status = 'open'
        ORDER BY g.embedding <=> $1::vector
        LIMIT $2;
    """
    # TODO: implement with Supabase RPC
    return []
