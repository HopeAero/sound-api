import uuid
import shutil
import librosa
import numpy as np
import tensorflow as tf
from keras.models import load_model
import pandas as pd
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
    ambiental = "ambiental"
    animal = "animal"
    musica = "musica"
    

def test_audio(file_path, model, target_shape):
    # Load and preprocess the audio file
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
    mel_spectrogram = tf.image.resize(np.expand_dims(mel_spectrogram, axis=-1), target_shape)
    mel_spectrogram = tf.reshape(mel_spectrogram, (1,) + target_shape + (1,))
    
    # Make predictions
    predictions = model.predict(mel_spectrogram)
    
    # Get the class probabilities
    class_probabilities = predictions[0]
    
    # Get the predicted class index
    predicted_class_index = np.argmax(class_probabilities)
    
    return class_probabilities, predicted_class_index

def predict_sound(file_path, model, target_shape, classes):
    
    class_probabilities, predicted_class_index = test_audio(file_path, model, target_shape)
    
    for i, class_label in enumerate(classes):
        probability = class_probabilities[i]
        print(f'Clase: {class_label}, Probabilidad: {probability:.4f}')

    # Calculate and display the predicted class and accuracy
    predicted_class = classes[predicted_class_index]
    accuracy = class_probabilities[predicted_class_index]
    
    return predicted_class, accuracy
    

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
    sound_path = f"app/sounds/{tag}/{id}.wav"
    with Path(sound_path).open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    sound = schemas.SoundCreate.model_construct(
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

    db_sound = create_sound(db, sound)

    return db_sound

