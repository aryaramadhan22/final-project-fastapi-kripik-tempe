from typing import Literal, Optional
from pydantic import BaseModel, Field


# Auth

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# Game

PlatformType = Literal["pc", "mobile", "console"]
StatusType = Literal["wishlist", "playing", "completed"]


class GameBase(BaseModel):
    title: str = Field(..., max_length=100)
    genre: str = Field(..., max_length=50)
    platform: PlatformType
    status: StatusType
    hours_played: int = Field(default=0, ge=0)
    rating: int = Field(default=0, ge=0, le=10)
    review: Optional[str] = ""


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    platform: Optional[PlatformType] = None
    status: Optional[StatusType] = None
    hours_played: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=0, le=10)
    review: Optional[str] = None


class GameOut(GameBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
