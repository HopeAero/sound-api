import keras
from keras.layers import Activation, Dense, Dropout, Conv2D, Flatten
from keras.layers import MaxPooling2D, BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import h5py
import librosa
import librosa.display
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from keras.utils import plot_model
from sklearn.preprocessing import LabelEncoder


#%% Leemos los datos del archivo csv que viene en el paquete de datos
data = pd.read_csv('metadata/sound_metadata.csv')

#%% Calculamos el espectrograma de los archivos y los vamos añadiendo a la variable D
D=[]
max_length = 1292  # o cualquier otro número que elijas

# Crear un diccionario para mapear cada Clasificación única a un nuevo ID
clasificacion_to_id = {clasificacion: i+1 for i, clasificacion in enumerate(data['Clasificación'].unique())}

# Crear una nueva columna ID con los nuevos IDs
data['ID'] = data['Clasificación'].map(clasificacion_to_id)

for row in data.itertuples():
    audio_file_path = 'sound/' + row[2] + '/' + row[4]
    y, sr = librosa.load(audio_file_path, duration=30)
    s = librosa.feature.melspectrogram(y=y, sr=sr)
    ps = librosa.power_to_db(s)
    ps = ps.astype(np.float32)
    
    # Si ps es más corto que max_length, lo rellenamos con ceros
    if ps.shape[1] < max_length:
        ps = np.pad(ps, ((0, 0), (0, max_length - ps.shape[1])), 'constant')

    # Si ps es más largo que max_length, lo truncamos
    if ps.shape[1] > max_length:
        ps = ps[:, :max_length]
    
    D.append( (ps, row[1]) )
    
random.shuffle(D)

D_train=[]
D_valid=[]
D_test=[]

for i in range(len(D)):
    if i < 0.8*len(D):
        D_train.append(D[i])
    elif i < 0.9*len(D):
        D_valid.append(D[i])
    else:
        D_test.append(D[i])

        
#%% Preparamos el dataset, desordenando las muestras y separándolas en muestras para entrenar, para evaluar y para testear
dataset_train=D_train
dataset_valid=D_valid
dataset_test=D_test

random.shuffle(dataset_train)
random.shuffle(dataset_valid)
random.shuffle(dataset_test)

train=dataset_train
valid=dataset_valid
test=dataset_test

X_train, y_train = zip(*train)
X_valid, y_valid = zip(*valid)
X_test, y_test = zip(*test)

X_train = np.array([x.reshape( (128, 1292, 1) ) for x in X_train])
X_valid = np.array([x.reshape( (128, 1292, 1) ) for x in X_valid])
X_test = np.array([x.reshape( (128, 1292, 1) ) for x in X_test])


# Normalización
mean = np.mean(X_train, axis=0)
std = np.std(X_train, axis=0)
X_train = (X_train - mean)/std
X_valid = (X_valid - mean)/std
X_test = (X_test - mean)/std

y_train = np.array(keras.utils.to_categorical(y_train, 4))
y_valid = np.array(keras.utils.to_categorical(y_valid, 4))
y_test = np.array(keras.utils.to_categorical(y_test, 4))


#%% Construimos el modelo propuesto y lo compilamos
model = Sequential()
input_shape=(128, 1292, 1)
model.add(Conv2D(24, (5, 5), strides=(1, 1), input_shape=input_shape))
model.add(MaxPooling2D((4, 2), strides=(4, 2)))
model.add(Activation('relu'))
model.add(Conv2D(48, (5, 5), padding="valid"))
model.add(MaxPooling2D((4, 2), strides=(4, 2)))
model.add(Activation('relu'))
model.add(Conv2D(48, (5, 5), padding="valid"))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dropout(rate=0.5))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(4))  
model.add(Activation('softmax'))
adam = Adam(0.0001)
model.compile(
    optimizer=adam,
    loss="categorical_crossentropy",
    metrics=['accuracy'])

#%% Entrenamos el modelo
model.fit(
    x=X_train, 
    y=y_train,
    epochs=100, 
    batch_size=128,
    validation_data= (X_valid, y_valid),
    callbacks=[
        EarlyStopping(monitor='val_loss', patience=5),
        ModelCheckpoint('model.h5', monitor='val_loss', save_best_only=True)
    ]
)

#%% Mejor modelo
callbacks = [
    ModelCheckpoint(filepath='best_model.h5', verbose=1, monitor='val_loss', save_best_only=True, mode='min'),
    EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
]


history = model.fit(
    x=X_train,
    y=y_train,
    epochs=100,
    batch_size=128,
    validation_data= (X_valid, y_valid),
    callbacks=callbacks)

