from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str
    cap: str
    consent_geoloc: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    name: str
    cap: str
    fulfillment_pref: str
    consent_geoloc: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
