import subprocess

# Definir los nombres de los scripts a ejecutar
scripts = ["upload_storage_1.py",
           "delete_storage_1.py",
           "upload_storage_2.py",
           "delete_storage_2.py",]

# Lista para almacenar los procesos
processes = []

# Iniciar un proceso para cada script
for script in scripts:
    process = subprocess.Popen(["python", script])
    processes.append(process)

# Esperar a que todos los procesos terminen
for process in processes:
    process.wait()
