import time
import requests
import os
while True:
    try:
        print("Verificando la conexion a internet..")
        res = requests.get("https://www.google.com/")
        if res.status_code == 200:
            import os
            from PIL import Image, ImageTk
            import tkinter as tk
            from tkinter import ttk
            from packages import routes,telegram,interface
            from packages import id

            def show_images(image_folders, interval):
                global image_files, current_index, image_labels, name_labels
                image_files = []
                current_index = [0] * len(image_folders)
                image_labels = []
                name_labels = []

                root = tk.Tk()
                root.title("Imágenes")
                root.geometry("1410x620")

                for i, folder in enumerate(image_folders):
                    if i==0:
                        name_titulo = tk.Label(root, text="Estimador de precipitación", font=("Arial", 12))
                        name_titulo.grid(row=2, column=1, padx=10)
                    if i==1:
                        name_titulo = tk.Label(root, text="Incremento de vapor de agua", font=("Arial", 12))
                        name_titulo.grid(row=2, column=2, padx=10)
                    if i==2:
                        name_titulo = tk.Label(root, text="Altura de la base de la nube", font=("Arial", 12))
                        name_titulo.grid(row=2, column=3, padx=10)
                    if i==3:
                        name_titulo = tk.Label(root, text="Capas de nieve/nubes", font=("Arial", 12))
                        name_titulo.grid(row=2, column=4, padx=10)

                    style = ttk.Style()
                    style.configure('Negrita.TLabel',font=('Arial', 12, 'bold'))
                    # Titulo de proyecto
                    title = ttk.Label(root, text="Estación Alerta Temprana Atmosférica", style='Negrita.TLabel')
                    title.grid(row=1,column=1,columnspan=4)
                    
                    # Crea un widget Label para mostrar el nombre de la imagen
                    name_label = tk.Label(root, font=("Arial", 12))
                    name_label.grid(row=3, column=i+1, padx=10)
                    name_labels.append(name_label)

                    # Crea un widget Label para mostrar las imágenes
                    image_label = tk.Label(root)
                    image_label.grid(row=4, column=i+1, padx=10)
                    image_labels.append(image_label)

                    image_files.append(interface.get_image_files(folder))

                    #a qui va desde Crear cajas de texto para mostrar los mensajes
                    # Crear cajas de texto para mostrar los mensaje
                    message_box1 = tk.Text(root, height=5, width=30)
                    message_box1.grid(row=5, column=1, sticky="nsew", padx=5)
                    message_box1.config(state=tk.DISABLED)

                    message_box2 = tk.Text(root, height=5, width=30)
                    message_box2.grid(row=5, column=2, sticky="nsew", padx=5)
                    message_box2.config(state=tk.DISABLED)

                    message_box3 = tk.Text(root, height=5, width=30)
                    message_box3.grid(row=5, column=3, sticky="nsew", padx=5)
                    message_box3.config(state=tk.DISABLED)

                    message_box4 = tk.Text(root, height=5, width=30)
                    message_box4.grid(row=5, column=4, sticky="nsew", padx=5)
                    message_box4.config(state=tk.DISABLED)


                # Función para actualizar la imagen y el nombre mostrados
                def update_image(index):
                    global current_index, image_files

                    if len(image_files[index]) > 0:
                        image_path = image_files[index][current_index[index]]

                        # Verifica si el archivo de la imagen todavia existe
                        if os.path.exists(image_path):
                            # Redimensionar las imágenes de la carpeta 3 y 4
                            if index == 2 or index == 3:
                                image = interface.resize_image(image_path, width=320, height=440)
                            else:
                                image = Image.open(image_path)

                            photo = ImageTk.PhotoImage(image)
                            image_labels[index].configure(image=photo)
                            image_labels[index].image = photo

                            # Obtiene el nombre de la imagen actual
                            image_name = os.path.splitext(os.path.basename(image_path))[0]
                            #image_name = os.path.basename(image_path)
                            name_labels[index].configure(text=image_name)

                            # Incrementa el índice o restablece a cero si alcanza la última imagen
                            current_index[index] = (current_index[index] + 1) % len(image_files[index])
                        else:
                            # Si el archivo de imagen fue eliminado, pasa al siguiente
                            current_index[index] = (current_index[index] + 1) % len(image_files[index])
                            update_image(index)

                    else:
                        # Si no hay imágenes en la carpeta, muestra un mensaje
                        image_labels[index].configure(image=None)
                        name_labels[index].configure(text="No hay imágenes")

                    # Obtén la lista actualizada de archivos de imagen
                    new_image_files = interface.get_image_files(image_folders[index])

                    # Compara la lista actualizada con la anterior para detectar cambios
                    if image_files[index] != new_image_files:
                        image_files[index] = new_image_files
                        current_index[index] = 0

                    # Programa la siguiente actualización de imagen después del intervalo especificado
                    root.after(interval, update_image, index)

                # Inicia la secuencia de imágenes para cada carpeta
                for i in range(len(image_folders)):
                    update_image(i)  

                #aqui iba la funcion entera update_message_boxes()
                def update_message_boxes():
                    updates = telegram.get_updates()
                    last_id = telegram.get_last_id()
                    if(last_id==id.Luis() or last_id==id.Elmer()):
                        messages = telegram.get_all_messages(updates, last_id)  # Coloca tu propio ID aquí

                        for i, message_box in enumerate([message_box1, message_box2, message_box3, message_box4]):
                                message_text = messages[i]
                                message_box.config(state=tk.NORMAL)
                                message_box.delete('1.0', tk.END)
                                message_box.insert(tk.END, message_text)
                                message_box.config(state=tk.DISABLED)
                                message_box.yview(tk.END)

                        # Programar la próxima actualización después de 1 segundo
                        root.after(1000, update_message_boxes)

                update_message_boxes()
                root.mainloop()


            image_folders = [
                routes.R1I(),
                routes.R2I(),
                routes.R3I(),
                routes.R4I()
            ]

            interval = 1000
            show_images(image_folders, interval)


    except Exception as e:
        print(f"Se perdio la conexion a internet..{e}")

    time.sleep(1) 
