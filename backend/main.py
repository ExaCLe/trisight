import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.database import engine
from backend.item_config.api_item_config import router as item_config_router
from backend.item_config_results.api_item_config_result import (
    router as item_config_result_router,
)
from backend.models import Base
from backend.test_config.api_test_config import router as test_config_router
from backend.test_config_results.api_test_config_results import (
    router as test_config_result_router,
)
from backend.user.api_user import router as user_router, init_oauth
from dotenv import load_dotenv


load_dotenv()

init_oauth()

app = FastAPI()

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
