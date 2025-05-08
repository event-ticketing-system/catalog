from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.routers import catalog

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
    "http://localhost:3000"
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
