# Script para comentar 
"""
Ejemplos:
enviar("producto_uno","Información sobre el producto uno")
enviar("producto_dos","Información sobre el producto dos")
enviar("producto_tres","Información sobre el producto tres")
enviar("producto_cuatro","Información sobre el producto cuatro")
enviar("producto_cinco","Información sobre el producto cinco")

Nota: key.json debe estar dentro de la carpeta Emision
"""
import firebase_admin
from firebase_admin import credentials, db
import datetime 
import pytz
import os
import time
import urllib3.exceptions
import requests.exceptions
from dotenv import load_dotenv
load_dotenv() # carga variables de .env

# encontrar el key.json
key_path = 'key.json'
if not os.path.exists(key_path):
  key_path = os.path.join('Emision', key_path)

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

# Especificar URL de la base de datos
db_url = os.getenv("DB_URL")
ref = db.reference(url=db_url) 

def enviar(tipo,texto):
    paragraph = texto
    # Establecer zona horaria de Peru
    peru_tz = pytz.timezone('America/Lima')

    ref.child("comentarios").child(tipo).set({
        'texto': paragraph,
        'fecha': datetime.datetime.now(tz=peru_tz).isoformat()
    })

def recibir(tipo):
  try:
    data = ref.child("comentarios").child(tipo).get()

    if data:
      texto = data['texto']
      fecha = data['fecha']
      return texto,fecha
    else:
      return "No hay datos", "No hay datos"
  
  except (urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError) as e:
      print("Error de conexión:", e)
      print("Reintentando en 5 segundos...")
      time.sleep(5)  # Esperar 5 segundos antes de reintentar
      return recibir(tipo)  # Volver a llamar a la función

