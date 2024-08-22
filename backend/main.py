from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.item_config.api_item_config import router as item_config_router
from backend.item_config_results.api_item_config_result import router as item_config_result_router
from backend.models import Base
from backend.test_config.api_test_config import router as test_config_router
from backend.test_config_results.api_test_config_results import router as test_config_result_router

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
app.include_router(test_config_router, prefix='/api/test_configs')
app.include_router(test_config_result_router, prefix='/api/test_config_results')
