import csv
import hashlib
import os
import uuid

# Ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta de la carpeta "sound"
sound_folder = os.path.join(current_dir, "../sound")

# Ruta del directorio "metadata"
metadata_dir = os.path.join(current_dir, "app", "metadata")

# Crear el directorio "metadata" si no existe
os.makedirs(metadata_dir, exist_ok=True)

# Ruta del archivo CSV de salida
csv_file = os.path.join(metadata_dir, "sound_metadata.csv")

# Obtener la lista de carpetas de clasificación en la carpeta "sound"
classification_folders = os.listdir(sound_folder)

# Diccionario para almacenar la información de cada archivo y su ID de combinación
file_combinations = {}

# Abrir el archivo CSV para escribir
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escribir encabezados en el archivo CSV
    writer.writerow(["id", "clasificación", "splitId", "nombre-de-archivo", "tamaño"])

    # Escribir información de cada archivo en el archivo CSV
    for classification_folder in classification_folders:
        classification_path = os.path.join(sound_folder, classification_folder)
        if os.path.isdir(classification_path):
            audio_files = os.listdir(classification_path)
            for audio_file in audio_files:
                file_path = os.path.join(classification_path, audio_file)
                file_size = os.path.getsize(file_path)
                split_id = audio_file.split("_")[-1].split(".")[0]  # Obtener el SplitId del nombre del archivo

                # Generar el ID de combinación utilizando una parte del nombre del archivo que sea la misma para todos los archivos que forman parte del mismo audio
                base_name = "_".join(audio_file.split("_")[:-1])
                combination_id = int(hashlib.sha256(base_name.encode()).hexdigest(), 16) % 1000000

                # Almacenar la información del archivo y su ID de combinación en el diccionario
                if combination_id not in file_combinations:
                    file_combinations[combination_id] = []

                file_combinations[combination_id].append({
                "classification": classification_folder,
                "split_id": split_id,
                "file_name": audio_file,
                "file_size": file_size
                })

    # Escribir la información de cada archivo en el archivo CSV
    for combination_id, files in file_combinations.items():
        for file_info in files:
            writer.writerow([combination_id, file_info["classification"], file_info["split_id"], file_info["file_name"], file_info["file_size"]])

print("Archivo CSV creado exitosamente.")
