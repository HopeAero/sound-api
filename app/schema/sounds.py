from fastapi import UploadFile
from pydantic import BaseModel


# base
class SoundBase(BaseModel):
    id: str
    category: str | None = None
    sound: str | None = None


# create
class SoundCreate(SoundBase):
    pass


# return after classifying
class SoundClassifying():
    category: str | None = None


# read/return
class Sound(SoundBase):
    pass

    class Config:
        from_attributes = True