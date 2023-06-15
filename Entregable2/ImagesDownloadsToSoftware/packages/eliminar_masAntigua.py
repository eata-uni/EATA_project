import os
from datetime import datetime, timedelta
def eliminar_antigua(i):
    if i==1:
        # Ruta de la carpeta
        carpeta = 'C:/Users/Luis Chanquetti/Desktop/ImagesforInterface/type1/'
    if i==2:
        # Ruta de la carpeta
        carpeta = 'C:/Users/Luis Chanquetti/Desktop/ImagesforInterface/type2/'
    if i==3:
        # Ruta de la carpeta
        carpeta = 'C:/Users/Luis Chanquetti/Desktop/ImagesforInterface/type3/'
    if i==4:
        # Ruta de la carpeta
        carpeta = 'C:/Users/Luis Chanquetti/Desktop/ImagesforInterface/type4/'

    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(carpeta)

    # Filtrar solo los archivos .png
    archivos_png = [archivo for archivo in archivos if archivo.endswith('.png')]

    # Convertir los nombres de archivo en fechas
    fechas = [datetime.strptime(archivo.split('.')[0], '%Y-%m-%d %H-%M-%S') for archivo in archivos_png]

    # Obtener la fecha de ayer
    fecha_ayer = datetime.now().date() - timedelta(days=1)

    # Filtrar las fechas que corresponden a ayer
    fechas_ayer = [fecha for fecha in fechas if fecha.date() == fecha_ayer]

    # Encontrar la imagen más antigua de ayer
    if fechas_ayer:
        imagen_mas_antigua_ayer = min(fechas_ayer)

        # Obtener el nombre de archivo correspondiente a la imagen más antigua de ayer
        nombre_imagen_mas_antigua_ayer = imagen_mas_antigua_ayer.strftime('%Y-%m-%d %H-%M-%S.png')

        # Eliminar la imagen más antigua de ayer
        ruta_imagen_mas_antigua_ayer = os.path.join(carpeta, nombre_imagen_mas_antigua_ayer)
        os.remove(ruta_imagen_mas_antigua_ayer)

    print(f"La imagen del tipo {i} más antigua del día anterior ha sido eliminada.")
