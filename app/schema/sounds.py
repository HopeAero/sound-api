from enum import Enum
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class TagEnum(str, Enum):
    ambiental = "ambiental"
    animal = "animal"
    musica = "musica"


# base
class SoundBase(BaseModel):
    id: UUID
    work_id: Optional[UUID] = None
    type: str
    description: str
    tag: TagEnum
    source: str
    copyright: str
    reference: str
    author_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None


# create
class SoundCreate(SoundBase):
    pass


# read/return
class Sound(SoundBase):
    class Config:
        from_attributes = True