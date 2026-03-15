from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # "artist" | "business"
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(body: SignUpRequest):
    """
    Register a new user.
    TODO: call supabase.auth.sign_up() with email/password
    TODO: insert row into users table with role
    TODO: create corresponding artist_profiles or business_profiles row
    """
    return {"message": "signup placeholder", "email": body.email, "role": body.role}


@router.post("/login")
async def login(body: LoginRequest):
    """
    Authenticate a user.
    TODO: call supabase.auth.sign_in_with_password()
    TODO: return the Supabase session (access_token, refresh_token)
    """
    return {"message": "login placeholder", "email": body.email}


@router.post("/logout")
async def logout():
    """
    TODO: call supabase.auth.sign_out()
    TODO: invalidate session on client by clearing tokens
    """
    return {"message": "logout placeholder"}
