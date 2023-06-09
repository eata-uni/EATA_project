import imageio.v2 as imageio
from packages.delete_before import for_downloads_start_1,for_downloads_start_2,for_downloads_start_3,for_downloads_start_4
from packages.delete_0KB import start_1,start_2,start_3,start_4
from packages.download import descargar_carpeta
from packages.routes import R1L,R1D,R2L,R2D,R3L,R3D,R4L,R4D

def type1():
    # solo descarga si las imagenes pertenecen al dia actual
    descargar_carpeta(R1D(), R1L())
    start_1()
    for_downloads_start_1()

def type2():
    # solo descarga si las imagenes pertenecen al dia actual
    descargar_carpeta(R2D(), R2L())
    start_2()
    for_downloads_start_2()

def type3():
    # solo descarga si las imagenes pertenecen al dia actual
    descargar_carpeta(R3D(), R3L())
    start_3()
    for_downloads_start_3()

def type4():
    # solo descarga si las imagenes pertenecen al dia actual
    descargar_carpeta(R4D(), R4L())
    start_4()
    for_downloads_start_4()


