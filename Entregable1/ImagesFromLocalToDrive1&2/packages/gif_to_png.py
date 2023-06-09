from PIL import Image
import os
from datetime import datetime

#convierte las imagenes .gif a .png pero solo las actuales, y si ya estan en .png entonces no vuelve a convertirlas
def start_giftopng_1():
    ruta_carpeta_gif = 'C:/Users/Juan Palacios/Desktop/EATA-Project/Entregable1/Database_hydro/'
    ruta_carpeta_png = 'C:/Users/Juan Palacios/Desktop/Images-auto/type1/'
    fecha_actual = datetime.now().date()

    for archivo_gif in os.listdir(ruta_carpeta_gif):
        if archivo_gif.endswith('.gif'):
            nombre_archivo_sin_extension = os.path.splitext(archivo_gif)[0]
            ruta_archivo_png = os.path.join(ruta_carpeta_png, nombre_archivo_sin_extension + '.png')
            
            if not os.path.exists(ruta_archivo_png):
                ruta_archivo_gif = os.path.join(ruta_carpeta_gif, archivo_gif)
                fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_archivo_gif)).date()

                if fecha_modificacion == fecha_actual:
                    imagen = Image.open(ruta_archivo_gif)
                    imagen = imagen.convert('RGBA')
                    imagen.save(ruta_archivo_png, 'PNG')



def start_giftopng_2():
    ruta_carpeta_gif = 'C:/Users/Juan Palacios/Desktop/EATA-Project/Entregable1/Database/'
    ruta_carpeta_png = 'C:/Users/Juan Palacios/Desktop/Images-auto/type2/'
    fecha_actual = datetime.now().date()

    for archivo_gif in os.listdir(ruta_carpeta_gif):
        if archivo_gif.endswith('.gif'):
            nombre_archivo_sin_extension = os.path.splitext(archivo_gif)[0]
            ruta_archivo_png = os.path.join(ruta_carpeta_png, nombre_archivo_sin_extension + '.png')
            
            if not os.path.exists(ruta_archivo_png):
                ruta_archivo_gif = os.path.join(ruta_carpeta_gif, archivo_gif)
                fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_archivo_gif)).date()

                if fecha_modificacion == fecha_actual:
                    imagen = Image.open(ruta_archivo_gif)
                    imagen = imagen.convert('RGBA')
                    imagen.save(ruta_archivo_png, 'PNG')