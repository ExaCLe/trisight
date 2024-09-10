from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models, schemas


def create_test_config(db: Session, test_config: schemas.TestConfig, user: models.User):
    db_test_config = models.TestConfig(
        name=test_config.name,
        user_id=user.id,
        item_configs=db.query(models.ItemConfig)
        .filter(models.ItemConfig.id.in_(test_config.item_config_ids))
        .all(),
    )
    db.add(db_test_config)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    db.refresh(db_test_config)
    return db_test_config


def get_all_test_configs(db: Session):
    return db.query(models.TestConfig).all()


def get_test_config_by_id(db: Session, test_config_id: int):
    return (
        db.query(models.TestConfig)
        .filter(models.TestConfig.id == test_config_id)
        .first()
    )


def update_test_config(
    db: Session, test_config_id: int, test_config: schemas.TestConfig, user: models.User
):
    db_test_config = (
        db.query(models.TestConfig)
        .filter(models.TestConfig.id == test_config_id)
        .first()
    )
    if db_test_config:
        if db_test_config.user_id != user.id:
            raise HTTPException(
                status_code=401,
                detail=f"User {user.id} is not authorized to update test config {test_config_id}",
            )
        db_test_config.name = test_config.name
        db_test_config.item_configs = (
            db.query(models.ItemConfig)
            .filter(models.ItemConfig.id.in_(test_config.item_config_ids))
            .all()
        )
        db.commit()
        db.refresh(db_test_config)
    return db_test_config


def delete_test_config(db: Session, test_config_id: int, user: models.User):
    db_test_config = (
        db.query(models.TestConfig)
        .filter(models.TestConfig.id == test_config_id)
        .first()
    )
    if db_test_config:
        if db_test_config.user_id != user.id:
            raise HTTPException(
                status_code=401,
                detail=f"User {user.id} is not authorized to delete test config {test_config_id}",
            )
        db.delete(db_test_config)
        db.commit()
    return db_test_config
