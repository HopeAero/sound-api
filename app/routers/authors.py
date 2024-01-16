from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse

from app.db import SessionLocal
from app.schema import authors as schemas
from app.db import get_db
from app.services import authors as service


authors = APIRouter(prefix="/authors", tags=["authors"])


@authors.get(
    "/",
    description="Get a list of all authors",
)
def get_authors(db: SessionLocal = Depends(get_db)):
    authors = service.get_authors(db)
    return {"message": "lmao World", "authors": authors}


@authors.delete(
    "/{id}",
    description="Delete an author",
)
def delete_author(id: str, db: SessionLocal = Depends(get_db)):
    service.delete_author(db, id)
    return {"message": "author deleted", "id": id}


@authors.post(
    "/",
    description="Create an author",
)
def create_author(author: schemas.AuthorCreate, db: SessionLocal = Depends(get_db)):
    author = service.create_author(db, author)
    return {"message": "lmao World", "author": author}
