"""
Embedding service — wraps OpenAI text-embedding-3-small.

Usage:
    from services.embeddings import embed_text, embed_gig, embed_artist_profile
"""

import os
from openai import AsyncOpenAI

# TODO: load from .env via pydantic-settings
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536  # dimensions for text-embedding-3-small


async def embed_text(text: str) -> list[float]:
    """
    Generate an embedding vector for arbitrary text.
    Returns a list of floats (length = EMBEDDING_DIM).
    """
    # TODO: add retry logic / rate limit handling
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text.strip().replace("\n", " "),
    )
    return response.data[0].embedding


async def embed_gig(gig: dict) -> list[float]:
    """
    Build a natural-language description of a gig and embed it.
    The richer the text, the better the matching.
    """
    text = (
        f"{gig['title']}. "
        f"Category: {gig.get('category', '')}. "
        f"{gig.get('description', '')} "
        f"Location: {gig.get('location', 'Philadelphia')}. "
        f"Pay: {gig.get('pay', 'negotiable')}."
    )
    return await embed_text(text)


async def embed_artist_profile(profile: dict) -> list[float]:
    """
    Build a natural-language description of an artist and embed it.
    """
    skills_str = ", ".join(profile.get("skills", []))
    text = (
        f"{profile['display_name']} is a {profile.get('category', 'artist')} "
        f"based in {profile.get('location', 'Philadelphia')}. "
        f"{profile.get('bio', '')} "
        f"Skills: {skills_str}."
    )
    return await embed_text(text)
