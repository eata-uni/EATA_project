import os
import shutil
import time
from packages.routes import R1L,R1I,R2L,R2I,R3L,R3I,R4L,R4I
import threading

def start_1():
    # Carpeta de origen y carpeta de destino
    carpeta1 = R1L()
    carpeta2 = R1I()

    # Obtener la lista de imágenes iniciales en la carpeta1
    imagenes_carpeta1 = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]

    # Copiar todas las imágenes .png a la carpeta2
    for imagen in imagenes_carpeta1:
        origen = os.path.join(carpeta1, imagen)
        destino = os.path.join(carpeta2, imagen)
        shutil.copy(origen, destino)

    print('Imagenes copiadas correctamente a {}.'.format(carpeta1))

    while True:
        # Obtener la lista de imágenes actuales en la carpeta1
        imagenes_actuales = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]
        
        # Identificar las nuevas imágenes agregadas a la carpeta1
        nuevas_imagenes = set(imagenes_actuales) - set(imagenes_carpeta1)
        
        if nuevas_imagenes:
            time.sleep(5)
            # Mover las nuevas imágenes a la carpeta2
            for imagen in nuevas_imagenes:
                origen = os.path.join(carpeta1, imagen)
                destino = os.path.join(carpeta2, imagen)
                shutil.copy(origen, destino)
                time.sleep(1)
            
            print('Nuevas imagenes copiadas correctamente a {}.'.format(carpeta1))
            
            # Actualizar la lista de imágenes en la carpeta1
            imagenes_carpeta1 = imagenes_actuales
        
        # Esperar 1 segundo antes de verificar nuevamente
        time.sleep(1)

def start_2():
    print("Se ejecuto copy.start_2")
    carpeta1 = R2L()
    carpeta2 = R2I()

    # Obtener la lista de imágenes iniciales en la carpeta1
    imagenes_carpeta1 = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]

    # Copiar todas las imágenes .png a la carpeta2
    for imagen in imagenes_carpeta1:
        origen = os.path.join(carpeta1, imagen)
        destino = os.path.join(carpeta2, imagen)
        shutil.copy(origen, destino)


    print('Imagenes copiadas correctamente a {}.'.format(carpeta1))

    while True:
        # Obtener la lista de imágenes actuales en la carpeta1
        imagenes_actuales = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]
        
        # Identificar las nuevas imágenes agregadas a la carpeta1
        nuevas_imagenes = set(imagenes_actuales) - set(imagenes_carpeta1)
        
        if nuevas_imagenes:
            time.sleep(5)
            # Mover las nuevas imágenes a la carpeta2
            for imagen in nuevas_imagenes:
                origen = os.path.join(carpeta1, imagen)
                destino = os.path.join(carpeta2, imagen)
                shutil.copy(origen, destino)
                time.sleep(1)

            print('Nuevas imagenes copiadas correctamente a {}.'.format(carpeta1))
            
            # Actualizar la lista de imágenes en la carpeta1
            imagenes_carpeta1 = imagenes_actuales
        
        # Esperar 1 segundo antes de verificar nuevamente
        time.sleep(1)

def start_3():
    print("Se ejecuto copy.start_3")
    carpeta1 = R3L()
    carpeta2 = R3I()

    # Obtener la lista de imágenes iniciales en la carpeta1
    imagenes_carpeta1 = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]

    # Copiar todas las imágenes .png a la carpeta2
    for imagen in imagenes_carpeta1:
        origen = os.path.join(carpeta1, imagen)
        destino = os.path.join(carpeta2, imagen)
        shutil.copy(origen, destino)
        

    print('Imagenes copiadas correctamente a {}.'.format(carpeta1))

    while True:
        # Obtener la lista de imágenes actuales en la carpeta1
        imagenes_actuales = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]
        
        # Identificar las nuevas imágenes agregadas a la carpeta1
        nuevas_imagenes = set(imagenes_actuales) - set(imagenes_carpeta1)
        
        if nuevas_imagenes:
            time.sleep(5)
            # Mover las nuevas imágenes a la carpeta2
            for imagen in nuevas_imagenes:
                origen = os.path.join(carpeta1, imagen)
                destino = os.path.join(carpeta2, imagen)
                shutil.copy(origen, destino)
                time.sleep(1)

            print('Nuevas imagenes copiadas correctamente a {}.'.format(carpeta1))
            
            # Actualizar la lista de imágenes en la carpeta1
            imagenes_carpeta1 = imagenes_actuales
        
        # Esperar 1 segundo antes de verificar nuevamente
        time.sleep(1)

def start_4():
    print("Se ejecuto copy.start_4")
    carpeta1 = R4L()
    carpeta2 = R4I()

    # Obtener la lista de imágenes iniciales en la carpeta1
    imagenes_carpeta1 = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]

    # Copiar todas las imágenes .png a la carpeta2
    for imagen in imagenes_carpeta1:
        origen = os.path.join(carpeta1, imagen)
        destino = os.path.join(carpeta2, imagen)
        shutil.copy(origen, destino)
   
    print('Imagenes copiadas correctamente a {}.'.format(carpeta1))

    while True:
        # Obtener la lista de imágenes actuales en la carpeta1
        imagenes_actuales = [archivo for archivo in os.listdir(carpeta1) if archivo.endswith('.png')]
        
        # Identificar las nuevas imágenes agregadas a la carpeta1
        nuevas_imagenes = set(imagenes_actuales) - set(imagenes_carpeta1)
        
        if nuevas_imagenes:
            time.sleep(5)
            # Mover las nuevas imágenes a la carpeta2
            for imagen in nuevas_imagenes:
                origen = os.path.join(carpeta1, imagen)
                destino = os.path.join(carpeta2, imagen)
                shutil.copy(origen, destino)
                time.sleep(1)

            print('Nuevas imagenes copiadas correctamente a {}.'.format(carpeta1))
            
            # Actualizar la lista de imágenes en la carpeta1
            imagenes_carpeta1 = imagenes_actuales
        
        # Esperar 1 segundo antes de verificar nuevamente
        time.sleep(1)

def start_global():
    start1 = threading.Thread(target = start_1)
    start2 = threading.Thread(target = start_2)
    start3 = threading.Thread(target = start_3)
    start4 = threading.Thread(target = start_4)

    start1.start()
    start2.start()
    start3.start()
    start4.start()