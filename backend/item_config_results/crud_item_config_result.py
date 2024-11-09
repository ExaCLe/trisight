from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models, schemas


def create_item_config_result(
    db: Session, item_config_result: schemas.ItemConfigResult, user: models.User
):
    db_item_config_result = models.ItemConfigResult(
        **item_config_result.model_dump(), user_id=user.id
    )
    db.add(db_item_config_result)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    db.refresh(db_item_config_result)
    return db_item_config_result


def get_all_item_config_results_for_item_config(
    db: Session, item_config_id: int, user: models.User
):
    return (
        db.query(models.ItemConfigResult)
        .filter(
            models.ItemConfigResult.item_config_id == item_config_id,
            models.ItemConfigResult.user_id == user.id,
        )
        .all()
    )


def get_item_config_result_by_id(
    db: Session, item_config_result_id: int, user: models.User
):
    return (
        db.query(models.ItemConfigResult)
        .filter(models.ItemConfigResult.id == item_config_result_id)
        .first()
    )


def get_all_item_config_results_for_user(db: Session, user: models.User):
    print(user.id)
    return (
        db.query(models.ItemConfigResult)
        .filter(models.ItemConfigResult.user_id == user.id)
        .all()
    )
