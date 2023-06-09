import os
from datetime import datetime

#eliminar las imagenes del dia actual que pesen 0
def start_delete_1():
    carpeta = "C:/Users/Juan Palacios/Desktop/EATA-Project/Entregable1/Database_hydro/" 
    fecha_actual = datetime.now().date()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).date()

            if fecha_creacion == fecha_actual and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo: {ruta_archivo}")



                
def start_delete_2():                
    carpeta = "C:/Users/Juan Palacios/Desktop/EATA-Project/Entregable1/Database/"
    fecha_actual = datetime.now().date()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).date()

            if fecha_creacion == fecha_actual and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo: {ruta_archivo}")
            
                        
