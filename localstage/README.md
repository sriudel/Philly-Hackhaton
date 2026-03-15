# LocalStage

**A two-sided marketplace connecting local artists with Philly businesses.**

Artists browse gigs. Businesses find talent. Matching is powered by OpenAI embeddings — not keyword search.

---

## Architecture

```
┌─────────────────────┐       ┌──────────────────────┐
│   React + Vite      │──────▶│   FastAPI (Python)   │
│   Tailwind CSS      │  HTTP │   Uvicorn             │
│   localhost:5173    │       │   localhost:8000       │
└─────────────────────┘       └──────────┬───────────┘
                                          │
                               ┌──────────▼───────────┐
                               │  Supabase            │
                               │  ├─ Postgres         │
                               │  ├─ pgvector         │
                               │  └─ Auth (JWT)       │
                               └──────────────────────┘
                                          │
                               ┌──────────▼───────────┐
                               │  OpenAI API          │
                               │  text-embedding-3-   │
                               │  small (1536-dim)    │
                               └──────────────────────┘
```

### How matching works

1. When an artist creates/updates their profile, the backend generates an embedding from their bio + skills + category.
2. When a business posts a gig, the backend generates an embedding from the title + description.
3. Both vectors are stored in Supabase using the `pgvector` extension.
4. When an artist opens their feed, the backend queries `match_gigs()` — a Postgres function that returns gigs ordered by cosine similarity to the artist's embedding.
5. When a business views recommended artists, the backend calls `match_artists()` similarly.

No keyword matching, no tags — just semantic similarity.

---

## Project Structure

```
localstage/
├── frontend/               # React + Vite + Tailwind
│   ├── src/
│   │   ├── components/     # Navbar (shared UI)
│   │   ├── pages/          # Login, BusinessDashboard, ArtistFeed, PostGig
│   │   ├── App.jsx         # Routes + auth guard
│   │   ├── main.jsx
│   │   └── index.css       # Tailwind imports
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js      # Proxy /api → localhost:8000
│   ├── tailwind.config.js
│   └── .env.example
│
├── backend/                # FastAPI + Uvicorn
│   ├── main.py             # App entry, CORS, router registration
│   ├── routes/
│   │   ├── auth.py         # POST /auth/signup, /auth/login, /auth/logout
│   │   ├── gigs.py         # CRUD for gigs
│   │   ├── profiles.py     # Artist + business profile upsert
│   │   └── match.py        # Vector similarity endpoints
│   ├── services/
│   │   ├── embeddings.py   # OpenAI embedding generation
│   │   └── matching.py     # pgvector query helpers
│   ├── models/
│   │   ├── gig.py          # Pydantic models
│   │   └── profile.py
│   ├── db/
│   │   └── client.py       # Supabase client singleton
│   ├── requirements.txt
│   └── .env.example
│
└── db/
    └── schema.sql          # Supabase-ready Postgres schema + pgvector setup
```

---

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- A [Supabase](https://supabase.com) project (free tier works)
- An [OpenAI](https://platform.openai.com) API key

---

### 1. Database

1. Create a new Supabase project.
2. In the Supabase dashboard, go to **SQL Editor → New Query**.
3. Paste and run `db/schema.sql`.
4. Confirm the `vector` extension is enabled (Dashboard → Database → Extensions → search "vector").

---

### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY, JWT_SECRET

# Run dev server
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

---

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Fill in VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY

# Run dev server
npm run dev
```

App available at: http://localhost:5173

---

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/signup` | Register user (artist or business) |
| POST | `/auth/login` | Login, returns Supabase session |
| GET | `/gigs/` | List gigs (filter by business_id, category) |
| POST | `/gigs/` | Create gig + generate embedding |
| GET | `/profiles/artist/{user_id}` | Get artist profile |
| PUT | `/profiles/artist/{user_id}` | Upsert artist profile + re-embed |
| GET | `/match/gigs?artist_id=` | Top gigs for an artist (vector search) |
| GET | `/match/artists?gig_id=` | Top artists for a gig (vector search) |

---

## Git Workflow

We use a feature branch model. Main branch is always deployable.

```
main
├── feat/auth           # Supabase auth integration
├── feat/gig-crud       # Gig creation and listing
├── feat/embeddings     # OpenAI embedding + pgvector matching
├── feat/artist-feed    # Artist feed UI
└── feat/business-dash  # Business dashboard UI
```

**Branch naming:** `feat/<short-description>`, `fix/<short-description>`

**Commit style:** `feat: add gig creation endpoint`, `fix: correct CORS headers`

**PR process:** branch → PR → one review → squash merge to main

---

## Build Order (Recommended for Hackathon)

Work these in parallel across teammates:

| Priority | Task | Owner |
|----------|------|-------|
| 1 | Database schema + Supabase project setup | — |
| 2 | Backend auth routes (signup/login) | — |
| 2 | Frontend login page + Supabase client wiring | — |
| 3 | Gig CRUD (backend routes + frontend PostGig) | — |
| 3 | Artist/Business profile upsert | — |
| 4 | Embedding generation on gig create + profile save | — |
| 4 | pgvector match queries (Supabase RPC) | — |
| 5 | Wire match results into BusinessDashboard + ArtistFeed | — |
| 6 | Polish, error states, loading spinners | — |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Service role key (bypasses RLS — keep secret) |
| `OPENAI_API_KEY` | OpenAI API key |
| `JWT_SECRET` | Supabase JWT secret (for verifying tokens) |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon/public key (safe for client) |

---

## TODOs (search the codebase for `# TODO`)

Key ones to implement first:
- `backend/routes/auth.py` — wire up Supabase auth calls
- `backend/routes/match.py` — call `services/matching.py` with real embeddings
- `backend/services/matching.py` — implement Supabase RPC calls
- `frontend/src/App.jsx` — replace mock `useAuth` with real Supabase session
- `frontend/src/pages/ArtistFeed.jsx` — fetch from `/match/gigs`
- `frontend/src/pages/BusinessDashboard.jsx` — fetch from `/match/artists`
