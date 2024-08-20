from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from backend import schemas
from backend.item_config_crud import create_item_config, get_all_item_configs, delete_item_config, update_item_config, \
    get_item_config_by_id
from backend.utils import get_db

router = APIRouter()


# Endpoint to create a new item config
@router.post("/", response_model=schemas.ItemConfigResponse)
def create_item_config_endpoint(item_config: schemas.ItemConfig, db: Session = Depends(get_db)):
    return create_item_config(db=db, item_config=item_config)

# Endpoint to get all item configs
@router.get("/", response_model=list[schemas.ItemConfigResponse])
def read_all_item_configs_endpoint(db: Session = Depends(get_db)):
    return get_all_item_configs(db)

# Endpoint to get an item config by id
@router.get("/{item_config_id}", response_model=schemas.ItemConfigResponse)
def read_item_config_endpoint(item_config_id: int, db: Session = Depends(get_db)):
    todo = get_item_config_by_id(db, item_config_id=item_config_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Item Config with id {item_config_id} not found")
    return todo


# Endpoint to delete an item config by id
@router.delete("/{item_config_id}", response_model=schemas.ItemConfigResponse)
def delete_item_config_endpoint(item_config_id: int, db: Session = Depends(get_db)):
    todo = delete_item_config(db, item_config_id=item_config_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Item Config with id {item_config_id} not found")
    return todo


@router.put("/{item_config_id}", response_model=schemas.ItemConfigResponse)
def update_todo_endpoint(item_config_id: int, item_config: schemas.ItemConfig, db: Session = Depends(get_db)):
    updated_todo = update_item_config(db, item_config_id=item_config_id, item_config=item_config)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail=f"Item Config with id {item_config_id} not found")
    return updated_todo
