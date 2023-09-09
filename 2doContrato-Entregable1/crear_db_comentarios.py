import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Inicializa la aplicación de Firebase
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://eata-project-default-rtdb.firebaseio.com/'
})

# Referencia a la ubicación "comentarios"
comentarios_ref = db.reference('comentarios')

# Leer los departamentos desde el archivo de texto
with open('departamentos.txt', 'r') as file:
    departamentos = file.read().splitlines()

# Crear las variables dentro de cada departamento
for departamento in departamentos:
    producto_ref = comentarios_ref.child(f"producto_cuatro_{departamento}")
    producto_ref.update({
        "fecha": "",
        "texto": ""
    })
"""
# Eliminar las variables dentro de cada departamento
for departamento in departamentos:
    producto_ref = comentarios_ref.child(f"producto_uno_{departamento}")
    producto_ref.delete()
"""
print("Variables creadas exitosamente.")