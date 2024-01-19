from fastapi import APIRouter, Depends, File, UploadFile, Form
from uuid import UUID
from typing import Optional
from fastapi.responses import JSONResponse, FileResponse

from enum import Enum
import io
import os
from app.db.session import SessionLocal
from app.db.session import get_db
from app.services import multimedia as service
from app.schema.sounds import Sound as schemas

import librosa
import numpy as np
import tensorflow as tf
from keras.models import load_model
import pandas as pd
import tempfile



sounds = APIRouter(prefix="/sounds", tags=["sounds"])

class TagEnum(str, Enum):
    ambiental = "ambiental"
    animal = "animal"
    musica = "musica"

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

@sounds.post("/classify", description="Classify an sound")
async def classify_sound(
    file: UploadFile = File(...), db: SessionLocal = Depends(get_db)
):
    model = load_model('app/model/audio_classification_model.h5')
    target_shape = (128, 128)
    df = pd.read_csv('app/metadata/sound_metadata.csv')
    # Obtener las clases únicas
    classes = df['clasificación'].unique().tolist()
    
    try:
        file_contents = await file.read()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        
        temp_file.write(file_contents)
        temp_file.close()
        
        class_probabilities, predicted_class_index = service.test_audio(temp_file.name, model, target_shape)
        
        for i, class_label in enumerate(classes):
            probability = class_probabilities[i]
            print(f'Clase: {class_label}, Probabilidad: {probability:.4f}')

        # Calculate and display the predicted class and accuracy
        predicted_class = classes[predicted_class_index]
        accuracy = class_probabilities[predicted_class_index]
        
        print(f'El audio se clasifica como: {predicted_class}')
        print(f'Precision: {accuracy:.4f}')

        return JSONResponse(
            status_code=200,
            content={
                "message": "Sound successfully classified",
                "category": f"El audio se clasifica como: {predicted_class} con una precisión de {accuracy:.4f}",
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
    finally:
        # Elimina el archivo temporal
        os.unlink(temp_file.name)

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
        model = load_model('app/model/audio_classification_model.h5')
        target_shape = (128, 128)
        df = pd.read_csv('app/metadata/sound_metadata.csv')
        # Obtener las clases únicas
        classes = df['clasificación'].unique().tolist()
        
        file_contents = await file.read()
                        
        file_path = f"app/uploads/sound/{tag}/{id}/{file.filename}"

        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Guarda el contenido del archivo en el disco
        with open(file_path, "wb") as f:
            f.write(file_contents)
            
        print(f'Archivo guardado en: {file_path}')
        
        predicted_class, accuracy = service.predict_sound(file_path, model, target_shape, classes)
                
        tag = predicted_class    
        
        source = f"http://127.0.0.1:8000/{file_path}"          
            
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
            source,
        )
        return {"message": "Sound successfully created", "sound": db_sound}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
