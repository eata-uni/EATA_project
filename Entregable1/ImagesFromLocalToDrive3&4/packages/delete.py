import os
from datetime import datetime
def start_delete_3():
    carpeta = "C:/Users/Daniel Parado/Desktop/project_EATA_Lucas/Entregable1_extra/Database_producto_1/"
    fecha_actual = datetime.now().date()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).date()

            if fecha_creacion == fecha_actual and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo: {ruta_archivo}")


def start_delete_4():                
    carpeta = "C:/Users/Daniel Parado/Desktop/project_EATA_Lucas/Entregable1_extra/Database_producto_2/"
    fecha_actual = datetime.now().date()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).date()

            if fecha_creacion == fecha_actual and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo: {ruta_archivo}")


