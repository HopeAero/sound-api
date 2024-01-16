from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
from .config.config import settings
from app.models import authors, sounds, works, publications
from .db.session import engine, Base, SessionLocal


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    Base.metadata.create_all(bind=engine)
    return app


app = start_application()

@app.get("/")
def home():
    return {"msg":"Hello FastAPI🚀"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.get("/song")
async def get_song():
    return {"song": "song"}