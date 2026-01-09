from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base
from app.db.engine import engine
from app.routers import cats


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Spy Cat Agency API",
    description="Backend API for managing spy cats, missions and targets",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cats.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

