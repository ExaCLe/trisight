from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.item_config.api_item_config import router as item_config_router
from backend.item_config_results.api_item_config_result import router as item_config_result_router
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

app.include_router(item_config_router, prefix="/api/item_configs")
app.include_router(item_config_result_router, prefix="/api/item_config_results")
