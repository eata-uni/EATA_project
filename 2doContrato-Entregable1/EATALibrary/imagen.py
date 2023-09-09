from firebase_admin import credentials, storage, initialize_app

ruta_credenciales = 'key.json'
cred = credentials.Certificate(ruta_credenciales)
initialize_app(cred, {'storageBucket': 'eata-project.appspot.com'})

def subir(nombre_archivo, ruta_local, tipo):
    bucket = storage.bucket()
    destino = f"Images/{tipo}/{nombre_archivo}"  
    blob = bucket.blob(destino)
    blob.upload_from_filename(ruta_local)


def eliminar(carpeta):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=carpeta)
    for blob in blobs:
        if blob.name.endswith('/') or blob.name == carpeta:
            continue
        blob.delete()
        print(f"Imagen eliminada: {blob.name}")




