# LocalStage 🎸

A two-sided marketplace connecting local Philly artists with local businesses.
Artists browse gigs. Businesses find talent. Matching is powered by OpenAI embeddings — not keyword search.

---

## What each user sees

**Business owner** → `/business`
- Dashboard with active gigs + applicant count
- AI-recommended artists ranked by match score
- Post a Gig form — describe what you need, we match the right talent

**Artist** → `/artist`
- Feed of open gigs ranked by how well they fit your profile
- Match score on each card
- One-click apply

---

## Architecture

```
frontend/     React + Vite + Tailwind   → runs on http://localhost:5173
backend/      FastAPI + Uvicorn         → runs on http://localhost:8000
db/           Supabase Postgres + pgvector (hosted, no local DB needed)
```

**How matching works:**
1. Artist saves profile → backend embeds bio + skills via OpenAI
2. Business posts gig → backend embeds title + description via OpenAI
3. Artist opens feed → backend finds gigs by cosine similarity to artist's vector
4. Results ranked by score, no keywords involved

---

## Teammate Setup (no Docker)

### Step 1 — Get the code

```bash
# First time — clone the repo
git clone https://github.com/daniyar-udel/Philly-Hackhaton.git
cd Philly-Hackhaton

# Switch to the working branch
git checkout feat/localstage-scaffold
```

```bash
# Already cloned? Pull latest:
git fetch origin
git checkout feat/localstage-scaffold
git pull origin feat/localstage-scaffold
```

---

### Step 2 — Run the Frontend

**Check if you have Node.js:**
```bash
node --version   # need v18 or higher
```

**Don't have it? Install:**
```bash
# Mac
brew install node

# Windows → download LTS from https://nodejs.org
```

**Start the app:**
```bash
cd frontend
npm install
cp .env.example .env      # fill in Supabase keys (get from teammate who set up DB)
npm run dev
```

Open → **http://localhost:5173**

> **Preview without keys:** open `frontend/src/App.jsx`, find `DEMO_ROLE` at the top,
> set it to `'business'` or `'artist'`. The app will skip login and go straight to that view.

---

### Step 3 — Run the Backend

**Check Python version:**
```bash
python3 --version   # need 3.11 or higher
```

```bash
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate      # Mac / Linux
venv\Scripts\activate         # Windows

# Install packages
pip install -r requirements.txt

# Set up env
cp .env.example .env          # fill in keys (see below)

# Start the server
uvicorn main:app --reload --port 8000
```

Swagger API docs → **http://localhost:8000/docs**

---

### Step 4 — Database (one person does this once)

1. Create a free project at https://supabase.com
2. Go to **SQL Editor → New Query**
3. Paste the full contents of `db/schema.sql` and click Run
4. Go to **Settings → API** and grab:
   - Project URL → share as `SUPABASE_URL`
   - `anon` key → share as `SUPABASE_ANON_KEY` (frontend)
   - `service_role` key → share as `SUPABASE_SERVICE_KEY` (backend, keep secret)

---

## Environment Variables

**`backend/.env`** (copy from `backend/.env.example`)
```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
OPENAI_API_KEY=sk-...
JWT_SECRET=your-supabase-jwt-secret
ENVIRONMENT=development
```

**`frontend/.env`** (copy from `frontend/.env.example`)
```
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
VITE_API_BASE_URL=http://localhost:8000
```

---

## Git Workflow

```bash
# Start a new feature
git checkout feat/localstage-scaffold   # our base branch
git pull origin feat/localstage-scaffold
git checkout -b feat/your-feature

# Commit and push
git add .
git commit -m "feat: describe what you built"
git push origin feat/your-feature

# Open a PR on GitHub targeting feat/localstage-scaffold (not main)
```

**Branch naming:** `feat/thing-you-built`, `fix/bug-you-fixed`

---

## Build Order

| Priority | Task | File(s) |
|----------|------|---------|
| 1 | Set up Supabase + run schema.sql | `db/schema.sql` |
| 2 | Wire backend auth to Supabase | `backend/routes/auth.py` |
| 2 | Wire frontend login to Supabase | `frontend/src/App.jsx`, `pages/Login.jsx` |
| 3 | Gig CRUD (create, list, view) | `backend/routes/gigs.py` |
| 3 | Artist/Business profile upsert | `backend/routes/profiles.py` |
| 4 | Generate embeddings on save | `backend/services/embeddings.py` |
| 4 | pgvector match queries | `backend/services/matching.py` |
| 5 | Wire real data into feed + dashboard | `pages/ArtistFeed.jsx`, `BusinessDashboard.jsx` |
| 6 | Polish, loading states, error handling | everywhere |

Search the codebase for `# TODO` to find every stub that needs real logic.

---

## Project Structure

```
frontend/
  src/
    components/     Navbar
    pages/          Login, BusinessDashboard, ArtistFeed, PostGig
    App.jsx         Routes + auth (set DEMO_ROLE here to preview UI)
    main.jsx

backend/
  main.py           FastAPI app entry, CORS, router registration
  routes/           auth.py  gigs.py  profiles.py  match.py
  services/         embeddings.py (OpenAI)  matching.py (pgvector)
  models/           gig.py  profile.py
  db/               client.py (Supabase singleton)
  requirements.txt

db/
  schema.sql        All tables + pgvector indexes + RPC match functions
```
