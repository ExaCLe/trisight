from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import schemas
from backend.utils import get_db
from . import crud_difficulty

router = APIRouter()


@router.get("/{difficulty}", response_model=List[schemas.ItemConfigResponse])
def get_item_configs(difficulty: str, limit: int = 500, db: Session = Depends(get_db)):
    """API endpoint to retrieve ItemConfigs for a given difficulty."""
    if difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=404, detail="Invalid difficulty level")
    item_configs = crud_difficulty.get_item_configs_by_difficulty(db, difficulty, limit)
    return item_configs
