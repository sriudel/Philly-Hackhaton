from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import gigs, profiles, match, auth

app = FastAPI(title="LocalStage API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/auth",     tags=["auth"])
app.include_router(gigs.router,     prefix="/gigs",     tags=["gigs"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
app.include_router(match.router,    prefix="/match",    tags=["match"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "localstage-api"}
