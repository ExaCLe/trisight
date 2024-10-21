import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from backend.database import engine, SessionLocal
from backend.item_config.api_item_config import router as item_config_router
from backend.item_config_results.api_item_config_result import (
    router as item_config_result_router,
)
from backend.difficulty.crud_difficulty import fill_item_configs
from backend.models import Base
from backend.test_config.api_test_config import router as test_config_router
from backend.test_config_results.api_test_config_results import (
    router as test_config_result_router,
)
from backend.user.api_user import router as user_router, init_oauth
from backend.difficulty.api_difficulty import router as difficulty_router
from backend.config import settings


load_dotenv()

init_oauth()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Fill item configs")
    db = SessionLocal()
    count = 10 if settings.testing else 10_000
    try:
        fill_item_configs(db, count)
        yield
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)

# Create the database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  # Update with your Nuxt.js origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(item_config_router, prefix="/api/item_configs")
app.include_router(item_config_result_router, prefix="/api/item_config_results")
app.include_router(test_config_router, prefix="/api/test_configs")
app.include_router(test_config_result_router, prefix="/api/test_config_results")
app.include_router(user_router, prefix="/api/users")
app.include_router(difficulty_router, prefix="/api/difficulty")
