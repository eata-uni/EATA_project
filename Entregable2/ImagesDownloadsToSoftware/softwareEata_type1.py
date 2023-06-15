import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from packages import routes, telegram, interface
from packages import id

def show_image(image_folder, interval):
    global image_files, current_index, image_label, name_label
    image_files = []
    current_index = 0

    root = tk.Tk()
    root.title("Software EATA")
    root.geometry("1410x155")

    name_titulo = tk.Label(root, text="Estimador de precipitación", font=("Arial", 12))
    name_titulo.grid(row=2, column=1, padx=10)

    style = ttk.Style()
    style.configure('Negrita.TLabel', font=('Arial', 12, 'bold'))

    # Titulo de proyecto
    title = ttk.Label(root, text="Estación Alerta Temprana Atmosférica", style='Negrita.TLabel')
    title.grid(row=1, column=1, columnspan=2)

    # Crea un widget Label para mostrar el nombre de la imagen
    name_label = tk.Label(root, font=("Arial", 12))
    name_label.grid(row=3, column=1, padx=10)

    # Crea un widget Label para mostrar la imagen
    image_label = tk.Label(root)
    image_label.grid(row=4, column=1, padx=10)

    image_files = interface.get_image_files(image_folder)

    # Crea una caja de texto para mostrar los mensajes
    message_box = tk.Text(root, height=5, width=30)
    message_box.grid(row=5, column=1, sticky="nsew", padx=5)
    message_box.config(state=tk.DISABLED)

    # Función para actualizar la imagen y el nombre mostrados
    def update_image():
        global current_index, image_files

        if len(image_files) > 0:
            image_path = image_files[current_index]

            # Verifica si el archivo de la imagen todavía existe
            if os.path.exists(image_path):
                image = Image.open(image_path)

                photo = ImageTk.PhotoImage(image)
                image_label.configure(image=photo)
                image_label.image = photo

                # Obtiene el nombre de la imagen actual
                image_name = os.path.splitext(os.path.basename(image_path))[0]
                name_label.configure(text=image_name)

                # Incrementa el índice o restablece a cero si alcanza la última imagen
                current_index = (current_index + 1) % len(image_files)
            else:
                # Si el archivo de imagen fue eliminado, pasa al siguiente
                current_index = (current_index + 1) % len(image_files)
                update_image()

        else:
            # Si no hay imágenes en la carpeta, muestra un mensaje
            image_label.configure(image=None)
            name_label.configure(text="No hay imágenes")

        # Obtén la lista actualizada de archivos de imagen
        new_image_files = interface.get_image_files(image_folder)

        # Compara la lista actualizada con la anterior para detectar cambios
        if image_files != new_image_files:
            image_files = new_image_files
            current_index = 0

        # Programa la siguiente actualización de imagen después del intervalo especificado
        root.after(interval, update_image)

    # Inicia la secuencia de imágenes
    update_image()

    # Función para actualizar la caja de mensajes
    def update_message_box():
        updates = telegram.get_updates()
        last_id = telegram.get_last_id()
        if True:
            messages = telegram.get_all_messages(updates, last_id)  # Coloca tu propio ID aquí

            message_text = messages[0]  # Solo se muestra el mensaje correspondiente a la primera imagen

            message_box.config(state=tk.NORMAL)
            message_box.delete('1.0', tk.END)
            message_box.insert(tk.END, message_text)
            message_box.config(state=tk.DISABLED)
            message_box.yview(tk.END)

            # Programar la próxima actualización después de 1 segundo
            root.after(1000, update_message_box)

    # Inicia la actualización de la caja de mensajes
    update_message_box()

    root.mainloop()


image_folder = routes.R1I()
interval = 1000
show_image(image_folder, interval)

