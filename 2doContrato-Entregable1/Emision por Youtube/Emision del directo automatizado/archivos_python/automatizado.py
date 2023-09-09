
import subprocess
import pyautogui
import time
import pyperclip


while True:
    try:
        scripts = [
            "software.py",
            "abrir_obs.py",
            "iniciar_transmision.py",
            "finalizar_transmision.py"
        ]

        processes = []


        for script in scripts:
            process = subprocess.Popen(["python", script])
            processes.append(process)

        for process in processes:
            process.wait()

        time.sleep(86400)

    except Exception as e:
        print("ocurrio un error en automatizado.py: ",e)
