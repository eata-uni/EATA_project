from firebase_admin import credentials, storage, initialize_app, db
import os
import datetime 
import pytz

from dotenv import load_dotenv
is_dotenv = load_dotenv(dotenv_path="GOESutils\.env") # carga variables de .env
if not is_dotenv:
  is_dotenv = load_dotenv(dotenv_path="GOESutils/.env")

# encontrar el key.json
key_path = 'key.json'
if not os.path.exists(key_path):
  key_path = os.path.join("./GOESutils", key_path)

cred = credentials.Certificate(key_path)
initialize_app(cred, {'storageBucket': 'eata-project.appspot.com'})

# Especificar URL de la base de datos
db_url = os.getenv("DB_URL")
ref = db.reference(url=db_url) 

def UploadFile(full_local_path, destine_path, filename):
    bucket = storage.bucket()
    destine_path = destine_path.replace("\\", "/").replace(" ","_")
    filename = filename.replace(" ","_")
    full_destine_path = f"{destine_path}/{filename}"  
    # full_destine_path = os.path.join(destine_path, filename)
    blob = bucket.blob(full_destine_path)
    blob.upload_from_filename(full_local_path)
    print(f"File {os.path.basename(full_local_path)} uploaded to '{destine_path}' as {filename}")

def DeleteFile(carpeta):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=carpeta)
    for blob in blobs:
        if blob.name.endswith('/') or blob.name == carpeta:
            continue
        blob.delete()
        print(f"Imagen eliminada: {blob.name}")

def SendComments(tipo,texto):
    """
    Ejemplos:
    enviar("producto_uno","Información sobre el producto uno")
    enviar("producto_dos","Información sobre el producto dos")
    enviar("producto_tres","Información sobre el producto tres")
    enviar("producto_cuatro","Información sobre el producto cuatro")
    enviar("producto_cinco","Información sobre el producto cinco")

    Nota: key.json debe estar dentro de la carpeta Emision
    """
    paragraph = texto
    # Establecer zona horaria de Peru
    peru_tz = pytz.timezone('America/Lima')

    ref.child("comentarios").child(tipo).set({
        'texto': paragraph,
        'fecha': datetime.datetime.now(tz=peru_tz).isoformat()
    })

def GetComments(tipo):
  data = ref.child("comentarios").child(tipo).get()

  if data:
    texto = data['texto']
    fecha = data['fecha']
    return texto,fecha
  else:
    return "No hay datos", "No hay datos"




