from login import start_login
import os
from datetime import date

credenciales = start_login()

def subir_archivo(ruta_archivo, id_folder):
    archivo = None
    archivos_en_folder = credenciales.ListFile({'q': f"'{id_folder}' in parents and trashed=false"}).GetList()
    for file in archivos_en_folder:
        if file['title'] == ruta_archivo.split('/')[-1]:
            archivo = file
            break
    if archivo is None:
        archivo = credenciales.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': id_folder}]})
        archivo['title'] = ruta_archivo.split('/')[-1]
        archivo.SetContentFile(ruta_archivo)
        archivo.Upload()
    return archivo['id']

def subir_imagenes(ruta_local, id_folder):
    imagenes = [f for f in os.listdir(ruta_local) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif')]
    fecha_actual = date.today().strftime('%Y-%m-%d')
    for imagen in imagenes:
        ruta_imagen = os.path.join(ruta_local, imagen)
        fecha_imagen = date.fromtimestamp(os.path.getmtime(ruta_imagen)).strftime('%Y-%m-%d')
        if fecha_imagen == fecha_actual:
            subir_archivo(ruta_imagen, id_folder)


