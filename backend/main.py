from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.models import Base
from backend.todo_api import router as todo_router
from backend.item_config_api import router as item_config_router

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

app.include_router(todo_router, prefix="/api/todos")
app.include_router(item_config_router, prefix="/api/item_configs")
