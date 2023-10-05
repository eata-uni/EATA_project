import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
from datetime import datetime
import subprocess

folder_to_monitor = 'G:/Otros ordenadores/PC GERMAIN/ACHA_emision/'
destination_folder = 'C:/Users/Luis Chanquetti/Documents/Personal Projects/publicacion_automatizada/type1/'
python_script_path = 'C:/Users/Luis Chanquetti/Documents/Personal Projects/publicacion_automatizada/post.py'  # Reemplaza con la ruta real de tu script

class PNGHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.src_path.endswith('.png'):
            creation_date = datetime.fromtimestamp(os.path.getctime(event.src_path))
            today = datetime.today().date()
            if creation_date.date() == today:
                print(f'Nueva imagen PNG detectada y creada hoy: {event.src_path}')
                
                # Eliminar todas las imágenes .png en el directorio de destino
                for file in os.listdir(destination_folder):
                    if file.endswith('.png'):
                        file_path = os.path.join(destination_folder, file)
                        os.remove(file_path)
                        print(f'Eliminando: {file_path}')
                
                time.sleep(5)
                # Copiar la nueva imagen
                shutil.copy(event.src_path, destination_folder)

                # Ejecutar el código Python después de copiar
                subprocess.run(['python', python_script_path])

event_handler = PNGHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_monitor, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
