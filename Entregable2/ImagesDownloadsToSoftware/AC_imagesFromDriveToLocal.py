import time
import requests
import os
while True:
    try:
        print("Verificando la conexion a internet..")
        res = requests.get("https://www.google.com/")
        if res.status_code == 200:
            os.system(f'python imagesFromDriveToLocal.py')
    except Exception as e:
        print(f"Se perdio la conexion a internet..{e}")

    time.sleep(1) 