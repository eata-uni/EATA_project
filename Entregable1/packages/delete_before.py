# Este código elimina las imagenes que sean de dias anteriores a la fecha de hoy
import os
from datetime import datetime
from packages.routes import R1L,R1I,R2L,R2I,R3L,R3I,R4L,R4I
import threading

def for_downloads_start_1():
    carpeta = R1L() 

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de type1: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
                pass
    

def for_downloads_start_2():
    carpeta = R2L()   

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de type2: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
                pass
def for_downloads_start_3():
    carpeta = R3L()    

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de type3: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
                pass


def for_downloads_start_4():
    carpeta = R4L()    

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de type4: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
                pass

def for_interface_start_1():
    carpeta = R1I()   

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                    
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de ImagesforInterface/Type1: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
                
   


def for_interface_start_2():
    carpeta = R2I()      

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                    
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de ImagesforInterface/Type2: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")


def for_interface_start_3():
    carpeta = R3I()      

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                    
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de ImagesforInterface/Type3: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")


def for_interface_start_4():
    carpeta = R4I()     

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta_archivo = os.path.join(carpeta, archivo)
            current_date = datetime.now().date()
            nombre_sin_extension = os.path.splitext(archivo)[0]  # Obtener el nombre sin extensión
            try:
                file_date = datetime.strptime(nombre_sin_extension, '%Y-%m-%d %H-%M-%S').date()
                    
                if file_date < current_date:
                    os.remove(ruta_archivo)
                    print(f"Se elimino la imagen antigua de ImagesforInterface/Type4: {archivo}")
            except ValueError:
                print(f"El archivo no sigue el formato esperado: {archivo}")
            
def start_global():
    fd1 = threading.Thread(target=for_downloads_start_1)
    fd2 = threading.Thread(target=for_downloads_start_2)
    fd3 = threading.Thread(target=for_downloads_start_3)
    fd4 = threading.Thread(target=for_downloads_start_4)

    fi1 = threading.Thread(target=for_interface_start_1)
    fi2 = threading.Thread(target=for_interface_start_2)
    fi3 = threading.Thread(target=for_interface_start_3)
    fi4 = threading.Thread(target=for_interface_start_4)

    fd1.start()
    fd2.start()
    fd3.start()
    fd4.start()

    fi1.start()
    fi2.start()
    fi3.start()
    fi4.start()