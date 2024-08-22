from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models, schemas


def create_test_config_result(db: Session, test_config_result: schemas.TestConfigResult):
    db_test_config_result = models.TestConfigResult(
        test_config_id=test_config_result.test_config_id,
        correct_answers=test_config_result.correct_answers,
        wrong_answers=test_config_result.wrong_answers,
        time=test_config_result.time,
        item_config_results=db.query(models.ItemConfigResult).filter(
            models.ItemConfigResult.id.in_(test_config_result.item_config_result_ids)).all()
    )
    db.add(db_test_config_result)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=f"Constraint error: {e.orig}")

    db.refresh(db_test_config_result)
    return db_test_config_result


def get_all_test_config_results_for_test_config(db: Session, test_config_id: int):
    return db.query(models.TestConfigResult).filter(models.TestConfigResult.test_config_id == test_config_id).all()


def get_test_config_result_by_id(db: Session, test_config_result_id: int):
    return db.query(models.TestConfigResult).filter(models.TestConfigResult.id == test_config_result_id).first()


def update_test_config_result(db: Session, test_config_result_id: int, test_config_result: schemas.TestConfigResult):
    db_test_config_result = db.query(models.TestConfigResult).filter(
        models.TestConfigResult.id == test_config_result_id).first()
    if db_test_config_result:
        db_test_config_result.correct_answers = test_config_result.correct_answers
        db_test_config_result.wrong_answers = test_config_result.wrong_answers
        db_test_config_result.time = test_config_result.time
        db_test_config_result.item_config_results = db.query(models.ItemConfigResult).filter(
            models.ItemConfigResult.id.in_(test_config_result.item_config_result_ids)).all()
        db.commit()
        db.refresh(db_test_config_result)
    else:
        raise HTTPException(status_code=404, detail="TestConfigResult not found")
    return db_test_config_result


def delete_test_config_result(db: Session, test_config_result_id: int):
    db_test_config_result = db.query(models.TestConfigResult).filter(
        models.TestConfigResult.id == test_config_result_id).first()
    if db_test_config_result:
        db.delete(db_test_config_result)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="TestConfigResult not found")
    return db_test_config_result
