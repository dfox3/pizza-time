from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import dfizza.models.pizza  # noqa: F401 - ensure models are registered before create_all
from dfizza.routers import pizza, ui

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


WEB_DIR = Path(__file__).parent.parent.parent / "web"

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(pizza.router)
app.include_router(ui.router)
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def serve_index():
    return FileResponse(WEB_DIR / "htmx" / "index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
