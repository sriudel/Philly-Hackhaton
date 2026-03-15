-- LocalStage — Supabase/Postgres Schema
-- Run this in your Supabase SQL editor (Dashboard > SQL Editor > New Query)
--
-- Prerequisites:
--   1. Enable pgvector extension (done via Supabase dashboard or line below)
--   2. Enable Supabase Auth (users table is managed by Supabase automatically)

-- ─────────────────────────────────────────────
-- Extensions
-- ─────────────────────────────────────────────
create extension if not exists vector;


-- ─────────────────────────────────────────────
-- Users (metadata on top of Supabase Auth)
-- ─────────────────────────────────────────────
create table if not exists public.users (
  id          uuid primary key references auth.users(id) on delete cascade,
  role        text not null check (role in ('artist', 'business')),
  created_at  timestamptz default now()
);

-- Allow users to read/update their own row
alter table public.users enable row level security;

create policy "Users can read their own record"
  on public.users for select
  using (auth.uid() = id);

create policy "Users can update their own record"
  on public.users for update
  using (auth.uid() = id);


-- ─────────────────────────────────────────────
-- Artist Profiles
-- ─────────────────────────────────────────────
create table if not exists public.artist_profiles (
  user_id         uuid primary key references public.users(id) on delete cascade,
  display_name    text not null,
  bio             text,
  category        text,                        -- e.g. "Jazz Musician", "Muralist"
  skills          text[] default '{}',         -- e.g. ARRAY['piano','improvisation']
  location        text,
  portfolio_url   text,
  instagram_handle text,
  embedding       vector(1536),               -- OpenAI text-embedding-3-small
  created_at      timestamptz default now(),
  updated_at      timestamptz default now()
);

alter table public.artist_profiles enable row level security;

-- Artists manage their own profile; businesses can read all
create policy "Artists manage own profile"
  on public.artist_profiles for all
  using (auth.uid() = user_id);

create policy "Businesses can view artist profiles"
  on public.artist_profiles for select
  using (
    exists (
      select 1 from public.users
      where id = auth.uid() and role = 'business'
    )
  );

-- Index for fast vector search
create index if not exists artist_profiles_embedding_idx
  on public.artist_profiles
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);


-- ─────────────────────────────────────────────
-- Business Profiles
-- ─────────────────────────────────────────────
create table if not exists public.business_profiles (
  user_id        uuid primary key references public.users(id) on delete cascade,
  business_name  text not null,
  description    text,
  industry       text,
  location       text,
  website        text,
  created_at     timestamptz default now(),
  updated_at     timestamptz default now()
);

alter table public.business_profiles enable row level security;

create policy "Businesses manage own profile"
  on public.business_profiles for all
  using (auth.uid() = user_id);

create policy "Artists can view business profiles"
  on public.business_profiles for select
  using (
    exists (
      select 1 from public.users
      where id = auth.uid() and role = 'artist'
    )
  );


-- ─────────────────────────────────────────────
-- Gigs
-- ─────────────────────────────────────────────
create table if not exists public.gigs (
  id           uuid primary key default gen_random_uuid(),
  business_id  uuid not null references public.users(id) on delete cascade,
  title        text not null,
  category     text,                           -- e.g. "Live Music", "Mural/Visual Art"
  description  text,
  pay          text,
  date         text,                           -- kept as text for flexibility (e.g. "Flexible")
  location     text,
  status       text not null default 'open'
                 check (status in ('open', 'filled', 'cancelled')),
  embedding    vector(1536),                   -- OpenAI text-embedding-3-small
  created_at   timestamptz default now(),
  updated_at   timestamptz default now()
);

alter table public.gigs enable row level security;

create policy "Businesses manage own gigs"
  on public.gigs for all
  using (auth.uid() = business_id);

create policy "Artists can view open gigs"
  on public.gigs for select
  using (
    status = 'open'
    and exists (
      select 1 from public.users
      where id = auth.uid() and role = 'artist'
    )
  );

create index if not exists gigs_embedding_idx
  on public.gigs
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create index if not exists gigs_status_idx
  on public.gigs (status);


-- ─────────────────────────────────────────────
-- Applications
-- ─────────────────────────────────────────────
create table if not exists public.applications (
  id          uuid primary key default gen_random_uuid(),
  gig_id      uuid not null references public.gigs(id) on delete cascade,
  artist_id   uuid not null references public.users(id) on delete cascade,
  status      text not null default 'pending'
                check (status in ('pending', 'accepted', 'rejected')),
  message     text,                            -- optional cover note from artist
  created_at  timestamptz default now(),
  unique (gig_id, artist_id)                  -- prevent duplicate applications
);

alter table public.applications enable row level security;

create policy "Artists manage own applications"
  on public.applications for all
  using (auth.uid() = artist_id);

create policy "Businesses view applications to their gigs"
  on public.applications for select
  using (
    exists (
      select 1 from public.gigs g
      where g.id = gig_id and g.business_id = auth.uid()
    )
  );

create policy "Businesses update application status"
  on public.applications for update
  using (
    exists (
      select 1 from public.gigs g
      where g.id = gig_id and g.business_id = auth.uid()
    )
  );


-- ─────────────────────────────────────────────
-- Supabase RPC Functions for pgvector matching
-- ─────────────────────────────────────────────

-- Match artists to a gig embedding
create or replace function match_artists(
  query_embedding vector(1536),
  match_count     int default 10
)
returns table (
  user_id         uuid,
  display_name    text,
  bio             text,
  category        text,
  skills          text[],
  location        text,
  portfolio_url   text,
  instagram_handle text,
  match_score     float
)
language sql stable
as $$
  select
    ap.user_id,
    ap.display_name,
    ap.bio,
    ap.category,
    ap.skills,
    ap.location,
    ap.portfolio_url,
    ap.instagram_handle,
    1 - (ap.embedding <=> query_embedding) as match_score
  from public.artist_profiles ap
  where ap.embedding is not null
  order by ap.embedding <=> query_embedding
  limit match_count;
$$;


-- Match gigs to an artist embedding
create or replace function match_gigs(
  query_embedding vector(1536),
  match_count     int default 10
)
returns table (
  id          uuid,
  business_id uuid,
  title       text,
  category    text,
  description text,
  pay         text,
  date        text,
  location    text,
  match_score float
)
language sql stable
as $$
  select
    g.id,
    g.business_id,
    g.title,
    g.category,
    g.description,
    g.pay,
    g.date,
    g.location,
    1 - (g.embedding <=> query_embedding) as match_score
  from public.gigs g
  where g.status = 'open'
    and g.embedding is not null
  order by g.embedding <=> query_embedding
  limit match_count;
$$;
