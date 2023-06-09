import time
from packages.login import start_login
from packages.routes import R1D,R2D,R3D,R4D
from packages.type import type1,type2,type3,type4

def start():
    credenciales = start_login()

    # ID de la carpeta type1 a monitorear
    folder_type1 = R1D()
    folder_type2 = R2D()
    folder_type3 = R3D()
    folder_type4 = R4D()

    query_type1 = f"'{folder_type1}' in parents and trashed = false"
    query_type2 = f"'{folder_type2}' in parents and trashed = false"
    query_type3 = f"'{folder_type3}' in parents and trashed = false"
    query_type4 = f"'{folder_type4}' in parents and trashed = false"
                    
    # Obtener los archivos actuales en la carpeta
    current_files_type1 = set()
    current_files_type2 = set()
    current_files_type3 = set()
    current_files_type4 = set()

    results_type1 = credenciales.ListFile({'q':query_type1}).GetList()
    results_type2 = credenciales.ListFile({'q':query_type2}).GetList()
    results_type3 = credenciales.ListFile({'q':query_type3}).GetList()
    results_type4 = credenciales.ListFile({'q':query_type4}).GetList()

    for item in results_type1:
        current_files_type1.add(item['id'])
    for item in results_type2:
        current_files_type2.add(item['id'])
    for item in results_type3:
        current_files_type3.add(item['id'])
    for item in results_type3:
        current_files_type3.add(item['id'])

    while True:
        try:
            new_files_type1 = set()
            new_files_type2 = set()
            new_files_type3 = set()
            new_files_type4 = set()

            query_type1 = f"'{folder_type1}' in parents and trashed = false"
            query_type2 = f"'{folder_type2}' in parents and trashed = false"
            query_type3 = f"'{folder_type3}' in parents and trashed = false"
            query_type4 = f"'{folder_type4}' in parents and trashed = false"

            results_type1 = credenciales.ListFile({'q':query_type1}).GetList()
            results_type2 = credenciales.ListFile({'q':query_type2}).GetList()
            results_type3 = credenciales.ListFile({'q':query_type3}).GetList()
            results_type4 = credenciales.ListFile({'q':query_type4}).GetList()

            for item in results_type1:
                new_files_type1.add(item['id'])
            for item in results_type2:
                new_files_type2.add(item['id'])
            for item in results_type3:
                new_files_type3.add(item['id'])
            for item in results_type4:
                new_files_type4.add(item['id'])

            # Verificar si hay nuevos archivos en la carpeta
            diff_type1 = new_files_type1 - current_files_type1
            diff_type2= new_files_type2 - current_files_type2
            diff_type3 = new_files_type3 - current_files_type3
            diff_type4 = new_files_type4 - current_files_type4

            if len(diff_type1) > 0:
                print("Se ha subido un nuevo archivo a la carpeta Type1.")
                current_files_type1 = current_files_type1.union(diff_type1)
                type1()
            if len(diff_type2) > 0:
                print("Se ha subido un nuevo archivo a la carpeta Type2.")
                current_files_type2 = current_files_type2.union(diff_type2)
                type2()
            if len(diff_type3) > 0:
                print("Se ha subido un nuevo archivo a la carpeta Type3.")
                current_files_type3 = current_files_type3.union(diff_type3)
                type3()
            if len(diff_type4) > 0:
                print("Se ha subido un nuevo archivo a la carpeta Type4.")
                current_files_type4 = current_files_type4.union(diff_type4)
                type4()

            time.sleep(1)
        except Exception as e:
            print(f"Ocurrio un error en check_newUploadImage: {e}")
            time.sleep(1)

