import uuid
import shutil
from pathlib import Path
from fastapi import Form, UploadFile, File
from sqlalchemy.orm import Session
from enum import Enum
from typing import Optional

from app.models.multimedia import Sound as Model
from app.schema import sounds as schemas


def get_sound(db: Session, id: str):
    return db.query(Model).filter(Model.id == id).first()


def get_sound_by_tag(db: Session, tag: str):
    print(tag)
    return db.query(Model).filter(Model.tag == tag).all()


def get_sounds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Model).offset(skip).limit(limit).all()


def create_sound(db: Session, sound: schemas.SoundCreate):
    db_sound = Model(**sound.model_dump())
    db.add(db_sound)
    db.commit()
    db.refresh(db_sound)
    return db_sound


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


def save_sound(
    db: Session,
    id: str,
    work_id: str,
    author_id: str,
    publication_id: str,
    type: str,
    description: str,
    tag: str,
    copyright: str,
    reference: str,
    file: UploadFile = File(...),
):
    sound_path = f"app/sounds/{tag}/{id}.jpg"
    with Path(sound_path).open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    image = schemas.SoundCreate.model_construct(
        id = id,
        work_id = work_id,
        author_id = author_id,
        publication_id = publication_id,
        type = type,
        description = description,
        tag = tag,
        copyright = copyright,
        reference = reference,
        source = sound_path,  
    )

    db_image = create_image(db, image)

    return db_image