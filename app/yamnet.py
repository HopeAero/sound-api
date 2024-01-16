import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv
import io
import soundfile as sf
from scipy.signal import resample

# Load the model.
model = hub.load('https://www.kaggle.com/models/google/yamnet/frameworks/TensorFlow2/variations/yamnet/versions/1')

# Input: 3 seconds of silence as mono 16 kHz waveform samples.
waveform = np.zeros(3 * 16000, dtype=np.float32)

# Run the model, check the output.
scores, embeddings, log_mel_spectrogram = model(waveform)
scores.shape.assert_is_compatible_with([None, 521])
embeddings.shape.assert_is_compatible_with([None, 1024])
log_mel_spectrogram.shape.assert_is_compatible_with([None, 64])

# Find the name of the class with the top score when mean-aggregated across frames.
def class_names_from_csv(class_map_csv_text):
  """Returns list of class names corresponding to score vector."""
  class_map_csv = io.StringIO(class_map_csv_text)
  class_names = [display_name for (class_index, mid, display_name) in csv.reader(class_map_csv)]
  class_names = class_names[1:]  # Skip CSV header
  return class_names
class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(tf.io.read_file(class_map_path).numpy().decode('utf-8'))

audio_path = '../sound/Animal/Jaguar_2.wav'

# Cargar el archivo de audio
audio, sample_rate = sf.read(audio_path)

# Convertir el audio a mono si es estéreo
if audio.ndim > 1:
    audio = np.mean(audio, axis=1)

# Asegurarse de que el audio tenga una frecuencia de muestreo de 16 kHz
if sample_rate != 16000:
    audio = resample(audio, int(len(audio) * 16000 / sample_rate))

# Convertir el audio a un arreglo de tipo float32
waveform = np.array(audio, dtype=np.float32)

# Asegurarse de que el audio tenga una duración de 3 segundos
if len(waveform) < 3 * 16000:
    padding = np.zeros(3 * 16000 - len(waveform), dtype=np.float32)
    waveform = np.concatenate([waveform, padding])

# Ejecutar el modelo y verificar la salida
scores, embeddings, log_mel_spectrogram = model(waveform)
print('')
classification = class_names[scores.numpy().mean(axis=0).argmax()]
print("La clasificación del sonido es:", classification)
