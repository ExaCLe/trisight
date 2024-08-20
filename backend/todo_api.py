from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from backend import schemas
from backend.database import SessionLocal
from backend.todo_crud import get_todos, delete_todo, create_todo
from backend.utils import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TodoResponse)
def create_todo_endpoint(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, todo=todo)


@router.get("/", response_model=list[schemas.TodoResponse])
def read_todos_endpoint(db: Session = Depends(get_db)):
    return get_todos(db)


@router.delete("/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    todo = delete_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
