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
