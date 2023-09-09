import subprocess
import time
import datetime

while True:
    try:
        # Obtener la hora actual
        hora_actual = datetime.datetime.now().time()
        if(hora_actual.strftime("%H:%M:%S")=='00:10:00'):
            time.sleep(5)
            # Ruta al archivo .bat que deseas ejecutar
            ruta_archivo_bat = r'C:/Users/Luis Chanquetti/Documents/Personal Projects/Emision del directo automatizado/archivos_batch/ejecutar_obs.bat'

            # Ejecuta el archivo .bat
            subprocess.call([ruta_archivo_bat], shell=True)

            # obs se abre con la misma dimension con la que se cerro la ultima vez
            
    except Exception as e:
        print("error",e)

