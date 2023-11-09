
import subprocess
import pyautogui
import time
import pyperclip

while True:
    try:
        scripts = [
            "software2-germain.py",
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

        time.sleep(5)
    except Exception as e:
        print(e)

