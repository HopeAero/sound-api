from fastapi import APIRouter, Depends, File, UploadFile, Form
from uuid import UUID
from typing import Optional
from fastapi.responses import JSONResponse, FileResponse

from enum import Enum
import io

from app.db.session import SessionLocal
from app.db.session import get_db
from app.services import multimedia as service
from app.schema.sounds import Sound as schemas

sounds = APIRouter(prefix="/sounds", tags=["sounds"])

class TagEnum(str, Enum):
    music = "music"
    animal = "animal"
    battles = "battles"
    bookcovers = "bookcovers"
    book_pages = "book_pages"
    foods = "foods"
    landscapes = "landscapes"
    maps = "maps"
    paintings = "paintings"
    people = "people"
    plants = "plants"
    rivers = "rivers"
    sculptures = "sculptures"
    stamps = "stamps"

@sounds.get(
    "/",
    description="Get a list of all sounds",
)
def get_sounds(db: SessionLocal = Depends(get_db)):
    try:
        sounds = service.get_sounds(db)
        return {"sounds": sounds}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


@sounds.get(
    "/tag/{tag}",
    description="Get a list of all sounds from a tag",
)
def get_sounds(tag: str, db: SessionLocal = Depends(get_db)):
    try:
        sounds = service.get_sound_by_tag(db, tag)
        return {"sounds": sounds}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )


@sounds.get("/{id}/file", description="Get a sound file by id")
async def get_sound_file(id: str, db: SessionLocal = Depends(get_db)):
    sound = service.get_sound(db, id) 
    return FileResponse(sound.source)

@sounds.post("/", description="Upload an sound")
async def create_sound(
    id: UUID = Form(...),
    work_id: Optional[UUID] = Form(None),
    author_id: Optional[UUID] = Form(None),
    publication_id: Optional[UUID] = Form(None),
    type: str = Form(...),
    description: str = Form(...),
    tag: TagEnum = Form(...),
    copyright: str = Form(...),
    reference: str = Form(...),
    file: UploadFile = File(...),
    db: SessionLocal = Depends(get_db),
):
    try:
        db_sound = service.save_sound(
            db,
            id,
            work_id,
            author_id,
            publication_id,
            type,
            description,
            tag,
            copyright,
            reference,
            file,
        )
        return {"message": "Sound successfully created", "sound": db_sound}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
