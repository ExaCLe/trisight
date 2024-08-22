from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from backend import schemas
from backend.item_config_results.crud_item_config_result import create_item_config_result, \
    get_all_item_config_results_for_item_config, get_item_config_result_by_id
from backend.utils import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ItemConfigResultResponse)
def create_item_config_result_endpoint(item_config_result: schemas.ItemConfigResult, db: Session = Depends(get_db)):
    return create_item_config_result(db=db, item_config_result=item_config_result)


@router.get("/item_config/{item_config_id}", response_model=list[schemas.ItemConfigResultResponse])
def read_all_item_config_results_for_item_config_endpoint(item_config_id: int, db: Session = Depends(get_db)):
    return get_all_item_config_results_for_item_config(db, item_config_id)


@router.get("/{item_config_result_id}", response_model=schemas.ItemConfigResultResponse)
def read_item_config_result_endpoint(item_config_result_id: int, db: Session = Depends(get_db)):
    item_config_result = get_item_config_result_by_id(db, item_config_result_id=item_config_result_id)
    if item_config_result is None:
        raise HTTPException(status_code=404, detail=f"Item Config Result with id {item_config_result_id} not found")
    return item_config_result
