import os

def for_downloads():
    escritorio = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    carpeta_principal = os.path.join(escritorio, 'ImagesDownloaded')
    subcarpetas = ['type1', 'type2', 'type3', 'type4']
    os.makedirs(carpeta_principal)

    for subcarpeta in subcarpetas:
        ruta_subcarpeta = os.path.join(carpeta_principal, subcarpeta)
        os.makedirs(ruta_subcarpeta)

def for_interface():
    escritorio = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    carpeta_principal = os.path.join(escritorio, 'ImagesforInterface')
    subcarpetas = ['type1', 'type2', 'type3', 'type4']
    os.makedirs(carpeta_principal)

    for subcarpeta in subcarpetas:
        ruta_subcarpeta = os.path.join(carpeta_principal, subcarpeta)
        os.makedirs(ruta_subcarpeta)
