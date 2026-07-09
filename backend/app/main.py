from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.services.storage_service import ensure_buckets


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_buckets()
    yield


app = FastAPI(title="Lipstick API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.auth import router as auth_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.history import router as history_router
from app.api.v1.profile import router as profile_router
from app.api.v1.lipsticks import router as lipsticks_router
from app.api.v1.images import router as images_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(lipsticks_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
