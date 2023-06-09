import os
import datetime
from datetime import datetime
from packages.login import start_login 
# Función para extraer la fecha de un nombre de archivo de imagen
def extraer_fecha(nombre_archivo):
    fecha_str = nombre_archivo.replace(".tif", "").replace(".png", "")
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H-%M-%S")
    return fecha


def descargar_carpeta(id_carpeta, ruta_descarga):
    credenciales = start_login()

    query = f"'{id_carpeta}' in parents and trashed = false"
    archivos = credenciales.ListFile({'q': query}).GetList()

    for archivo in archivos:
        nombre_archivo = archivo['title']
        ruta_archivo = os.path.join(ruta_descarga, nombre_archivo)
        fecha_archivo = extraer_fecha(nombre_archivo).date()
        fecha_actual = datetime.now().date()

        if fecha_archivo == fecha_actual:
            if not os.path.exists(os.path.join(ruta_descarga, nombre_archivo)):
                archivo.GetContentFile(ruta_archivo)
                print(f"Archivo {nombre_archivo} descargado exitosamente en {ruta_archivo}")
            else:
                #print(f"Archivo {nombre_archivo} ya existe en la carpeta local.")
                pass
        else:
            #print(f"Archivo {nombre_archivo} no es del dia actual, no se descargara.")
            pass
