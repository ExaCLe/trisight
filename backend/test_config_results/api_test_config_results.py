from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from backend import schemas
from backend.test_config_results.crud_test_config_results import create_test_config_result, \
    get_all_test_config_results_for_test_config, get_test_config_result_by_id, \
    update_test_config_result, delete_test_config_result
from backend.utils import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TestConfigResultResponse)
def create_test_config_result_endpoint(test_config_result: schemas.TestConfigResult, db: Session = Depends(get_db)):
    return create_test_config_result(db=db, test_config_result=test_config_result)


@router.get("/test_config/{test_config_id}", response_model=list[schemas.TestConfigResultResponse])
def read_all_test_config_results_for_test_config_endpoint(test_config_id: int, db: Session = Depends(get_db)):
    return get_all_test_config_results_for_test_config(db=db, test_config_id=test_config_id)


@router.get("/{test_config_result_id}", response_model=schemas.TestConfigResultResponse)
def read_test_config_result_by_id_endpoint(test_config_result_id: int, db: Session = Depends(get_db)):
    test_config_result = get_test_config_result_by_id(db, test_config_result_id=test_config_result_id)
    if test_config_result is None:
        raise HTTPException(status_code=404, detail="TestConfigResult not found")
    return test_config_result


@router.put("/{test_config_result_id}", response_model=schemas.TestConfigResultResponse)
def update_test_config_result_endpoint(test_config_result_id: int, test_config_result: schemas.TestConfigResult,
                                       db: Session = Depends(get_db)):
    return update_test_config_result(db=db, test_config_result_id=test_config_result_id,
                                     test_config_result=test_config_result)


@router.delete("/{test_config_result_id}", response_model=schemas.TestConfigResultResponse)
def delete_test_config_result_endpoint(test_config_result_id: int, db: Session = Depends(get_db)):
    return delete_test_config_result(db=db, test_config_result_id=test_config_result_id)
