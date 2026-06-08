from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import dfizza.models.pizza  # noqa: F401 - ensure models are registered before create_all
from dfizza.routers import pizza

# To switch to PostgreSQL, change the URL to:
# "postgresql+asyncpg://user:password@host/dbname"
DATABASE_URL = "sqlite+aiosqlite:///pizza.db"


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    app.state.db_engine = engine
    app.state.db_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    print("[STARTUP] Connected to database.")

    yield

    await engine.dispose()
    print("[SHUTDOWN] Closed database connection.")


app = FastAPI(lifespan=lifespan)
app.include_router(pizza.router)


@app.get("/", tags=["health"])
async def read_root(request: Request):
    async with request.app.state.db_session() as session:
        return {"status": "healthy", "database_ready": session is not None}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
