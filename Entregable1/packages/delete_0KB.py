import os
from packages.routes import R1L,R2L,R3L,R4L
def start_1():
    # elimino los que pesan 0 del producto 1
    carpeta = R1L()
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                #print(f"Se eliminó el archivo: {ruta_archivo}")

def start_2():
    # elimino los que pesan 0 del producto 2
    import os
    carpeta = R2L()
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                #print(f"Se eliminó el archivo: {ruta_archivo}")

def start_3():
    # elimino los que pesan 0 del producto 3
    import os
    carpeta = R3L()
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                #print(f"Se eliminó el archivo: {ruta_archivo}")

def start_4():
    # elimino los que pesan 0 del producto 4
    import os
    carpeta = R4L()
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_archivo) and os.path.getsize(ruta_archivo) == 0:
                os.remove(ruta_archivo)
                #print(f"Se eliminó el archivo: {ruta_archivo}")