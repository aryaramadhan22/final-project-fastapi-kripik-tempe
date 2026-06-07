from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import Game, User
from app.schemas import GameCreate, GameUpdate, GameOut
from app.core.deps import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=List[GameOut])
def list_games(
    q: Optional[str] = Query(None, description="Search by title"),
    platform: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    qs = db.query(Game).filter(Game.owner_id == current_user.id)
    if q:
        qs = qs.filter(Game.title.ilike(f"%{q}%"))
    if platform:
        qs = qs.filter(Game.platform == platform)
    if status:
        qs = qs.filter(Game.status == status)
    return qs.all()


@router.get("/{game_id}", response_model=GameOut)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    game = db.query(Game).filter(Game.id == game_id, Game.owner_id == current_user.id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=GameOut, status_code=201)
def create_game(
    payload: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    game = Game(**payload.model_dump(), owner_id=current_user.id)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@router.put("/{game_id}", response_model=GameOut)
def update_game(
    game_id: int,
    payload: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    game = db.query(Game).filter(Game.id == game_id, Game.owner_id == current_user.id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(game, field, value)
    db.commit()
    db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    game = db.query(Game).filter(Game.id == game_id, Game.owner_id == current_user.id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(game)
    db.commit()


@router.get("/stats/summary", tags=["stats"])
def stats_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    games = db.query(Game).filter(Game.owner_id == current_user.id).all()

    platform_count: dict = {}
    status_count: dict = {}
    genre_ratings: dict = {}

    for g in games:
        platform_count[g.platform] = platform_count.get(g.platform, 0) + 1
        status_count[g.status] = status_count.get(g.status, 0) + 1
        if g.genre:
            genre_ratings.setdefault(g.genre, []).append(g.rating)

    avg_by_genre = {
        genre: round(sum(ratings) / len(ratings), 2)
        for genre, ratings in genre_ratings.items()
    }

    return {
        "total": len(games),
        "platform_distribution": platform_count,
        "status_distribution": status_count,
        "avg_rating_by_genre": avg_by_genre,
        "total_hours": sum(g.hours_played for g in games),
    }
