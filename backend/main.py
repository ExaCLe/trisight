from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend import schemas
from backend.todo_crud import get_todos, delete_todo, create_todo
from backend.database import engine, SessionLocal
from backend.models import Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your Nuxt.js origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI"}


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new todo
@app.post("/api/todos/", response_model=schemas.TodoResponse)
def create_todo_endpoint(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, todo=todo)


# Endpoint to get all todos
@app.get("/api/todos/", response_model=list[schemas.TodoResponse])
def read_todos_endpoint(db: Session = Depends(get_db)):
    return get_todos(db)


# Endpoint to delete a todo by ID
@app.delete("/api/todos/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    todo = delete_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
