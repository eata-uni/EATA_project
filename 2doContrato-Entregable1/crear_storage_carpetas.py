import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Inicializa la aplicación de Firebase
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'eata-project.appspot.com'
})

# Referencia al bucket de almacenamiento
bucket = storage.bucket()

# Leer los departamentos desde el archivo de texto
with open('departamentos.txt', 'r') as file:
    departamentos = file.read().splitlines()

# Crear carpetas dentro de la carpeta "Images"
for departamento in departamentos:
    folder_path = f"Images/T4{departamento}/"
    dummy_blob = bucket.blob(folder_path)
    dummy_blob.upload_from_string('')  # Sube un archivo vacío para crear la carpeta

print("Carpetas creadas exitosamente.")
