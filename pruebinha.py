import librosa
import numpy as np
from keras.models import load_model

def predecir_audio(audio_path):
    model = load_model('model.h5')
    class_names = {0: "Ambiental", 1: "Animal", 2: "Musica"}

    # Cargamos el audio
    audio, sr = librosa.load(audio_path, sr=None)

    # Preprocesamos el audio
    melspec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
    melspec = librosa.power_to_db(melspec).astype(np.float32)

    # Aseguramos que el espectrograma tenga la misma forma que los datos de entrada del modelo
    melspec = melspec[:128, :1292]
    if melspec.shape != (128, 1292):
        melspec = np.pad(melspec, pad_width=((0, 128 - melspec.shape[0]), (0, 1292 - melspec.shape[1])))

    # Agregamos una dimensión extra para el canal
    melspec = melspec[..., np.newaxis]

    # Hacemos la predicción con el modelo
    prediction = model.predict(np.array([melspec]))
    print(prediction)

    # La predicción es un vector de probabilidades, así que tomamos la clase con la probabilidad más alta
    predicted_class = np.argmax(prediction)

    return [predicted_class]

audio_path = 'sound/Ambiental/Rio_1.wav'

predicted_class = predecir_audio(audio_path)
print(f"La clase predicha es: {predicted_class}")