from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models, schemas


def create_item_config(db: Session, item_config: schemas.ItemConfig):
    db_item_config = models.ItemConfig(
        **item_config.model_dump()
    )
    db.add(db_item_config)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    db.refresh(db_item_config)
    return db_item_config


def get_all_item_configs(db: Session):
    return db.query(models.ItemConfig).all()


def get_item_config_by_id(db: Session, item_config_id: int):
    return db.query(models.ItemConfig).filter(models.ItemConfig.id == item_config_id).first()


def update_item_config(db: Session, item_config_id: int, item_config: schemas.ItemConfig):
    db_item_config = db.query(models.ItemConfig).filter(models.ItemConfig.id == item_config_id).first()
    if db_item_config:
        db_item_config.triangle_size = item_config.triangle_size
        db_item_config.triangle_color = item_config.triangle_color
        db_item_config.circle_size = item_config.circle_size
        db_item_config.circle_color = item_config.circle_color
        db_item_config.time_visible_ms = item_config.time_visible_ms
        db_item_config.orientation = item_config.orientation
        db.commit()
        db.refresh(db_item_config)
    return db_item_config


def delete_item_config(db: Session, item_config_id: int):
    db_item_config = db.query(models.ItemConfig).filter(models.ItemConfig.id == item_config_id).first()
    if db_item_config:
        db.delete(db_item_config)

        # also delete all item config results associated with this item config
        db.query(models.ItemConfigResult).filter(models.ItemConfigResult.item_config_id == item_config_id).delete()

        db.commit()
    return db_item_config
