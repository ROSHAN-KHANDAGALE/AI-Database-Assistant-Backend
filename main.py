from fastapi import FastAPI
from backend.db import engine, Base
from backend.routers import queries
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings


allow_origins = settings.allowed_origins

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=' API', 
    description='An API that generates SQL queries based on user questions using a language model.', 
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(queries.router)

@app.get("/")
def root():
    return {"message": "Welcome to the SQL Query Generator API!"}