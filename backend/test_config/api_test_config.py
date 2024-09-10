from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from backend import schemas
from backend.test_config.crud_test_config import (
    create_test_config,
    get_all_test_configs,
    delete_test_config,
    update_test_config,
    get_test_config_by_id,
)
from backend.user.api_user import get_current_user
from backend.utils import get_db

router = APIRouter()


# Endpoint to create a new test config
@router.post("/", response_model=schemas.TestConfigResponse)
def create_test_config_endpoint(
    test_config: schemas.TestConfig,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_test_config(db=db, test_config=test_config, user=user)


# Endpoint to get all test configs
@router.get("/", response_model=list[schemas.TestConfigResponse])
def read_all_test_configs_endpoint(db: Session = Depends(get_db)):
    return get_all_test_configs(db)


# Endpoint to get a test config by id
@router.get("/{test_config_id}", response_model=schemas.TestConfigResponse)
def read_test_config_endpoint(test_config_id: int, db: Session = Depends(get_db)):
    test_config = get_test_config_by_id(db, test_config_id=test_config_id)
    if test_config is None:
        raise HTTPException(
            status_code=404, detail=f"Test Config with id {test_config_id} not found"
        )
    return test_config


# Endpoint to delete a test config by id
@router.delete("/{test_config_id}", response_model=schemas.TestConfigResponse)
def delete_test_config_endpoint(
    test_config_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    test_config = delete_test_config(db, test_config_id=test_config_id, user=user)
    if test_config is None:
        raise HTTPException(
            status_code=404, detail=f"Test Config with id {test_config_id} not found"
        )
    return test_config


# Endpoint to update a test config by id
@router.put("/{test_config_id}", response_model=schemas.TestConfigResponse)
def update_test_config_endpoint(
    test_config_id: int,
    test_config: schemas.TestConfig,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    updated_test_config = update_test_config(
        db, test_config_id=test_config_id, test_config=test_config, user=user
    )
    if updated_test_config is None:
        raise HTTPException(
            status_code=404, detail=f"Test Config with id {test_config_id} not found"
        )
    return updated_test_config
