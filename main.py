from fastapi import FastAPI

from api.routes import router
from infra.logging import setup_logging

setup_logging()

app = FastAPI(title="Dengue Monitor API", version="0.1.0")

app.include_router(router)
