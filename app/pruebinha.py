import librosa
import numpy as np
import tensorflow as tf
from keras.models import load_model
import pandas as pd

# Load the saved model
model = load_model('model/audio_classification_model.h5')

# Define the target shape for input spectrograms
target_shape = (128, 128)

df = pd.read_csv('metadata/sound_metadata.csv')

# Obtener las clases únicas
classes = df['clasificación'].unique().tolist()


# Function to preprocess and classify an audio file
def test_audio(file_path, model):
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

# Test an audio file
test_audio_file = '../sound/narracion/20poemastranvia_06_girondo_64kb.wav'
class_probabilities, predicted_class_index = test_audio(test_audio_file, model)

# Display results for all classes
for i, class_label in enumerate(classes):
    probability = class_probabilities[i]
    print(f'Clase: {class_label}, Probabilidad: {probability:.4f}')

# Calculate and display the predicted class and accuracy
predicted_class = classes[predicted_class_index]
accuracy = class_probabilities[predicted_class_index]
print(f'El audio se clasifica como: {predicted_class}')
print(f'Precision: {accuracy:.4f}')