import math
from tkinter import Entry, Tk, Label, Button, filedialog
from pydub import AudioSegment
import os

class AudioSplitterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Audio Splitter")

        self.label = Label(master, text="Seleccione el archivo de audio a dividir:")
        self.label.pack()
        
        self.select_button = Button(master, text="Seleccionar archivo", command=self.select_file)
        self.select_button.pack()

        self.label = Label(master, text="Escriba la clasificacion del audio:")
        self.label.pack()
        
        self.text_entry = Entry(master)  # Campo de entrada de texto
        self.text_entry.pack()

        self.split_button = Button(master, text="Dividir archivo", state="disabled", command=self.split_audio)
        self.split_button.pack()

    def select_file(self):
        filetypes = (("Archivos de audio", "*.mp3"), ("Todos los archivos", "*.*"))
        self.filepath = filedialog.askopenfilename(title="Seleccione un archivo de audio", filetypes=filetypes)
        if self.filepath:
            self.label.config(text=f"Archivo seleccionado: {self.filepath}")
            self.split_button.config(state="normal")

    def split_audio(self):
        audio = AudioSegment.from_file(self.filepath, format="mp3")
        audio_duration = len(audio)
        segment_duration = 30000  # 30 segundos
        num_segments = math.ceil(audio_duration / segment_duration)

        filename = os.path.splitext(os.path.basename(self.filepath))[0]
        output_folder = "sound" + "/" + self.text_entry.get()  # Nombre de la carpeta de salida
        os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta de salida si no existe

        for i in range(num_segments):
            start = i * segment_duration
            end = start + segment_duration
            segment = audio[start:end]
            output_filepath = os.path.join(output_folder, f"{filename}_{i+1}.wav")  # Cambiar la extensión a .wav
            segment.export(output_filepath, format="wav")  # Exportar como archivo .wav

        self.label.config(text="Archivo dividido en segmentos de " + str(segment_duration) +" y guardado en la carpeta 'salida'.")
        self.split_button.config(state="disabled")

root = Tk()
my_gui = AudioSplitterGUI(root)
root.mainloop()