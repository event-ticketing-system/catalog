import asyncio
from app.consumer import consume_events
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.routers import catalog

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    settings.CLIENT_ORIGIN,
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8001",
    "https://mercury-uat.phonepe.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


app.include_router(catalog.router, tags=['Catalog'], prefix='/api/catalog')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB Catalog"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_events())