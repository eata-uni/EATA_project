import os
import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from comentarios import recibir
import datetime

while True:
    try:
        # Obtener la hora actual
        hora_actual = datetime.datetime.now().time()
        #if(hora_actual.strftime("%H:%M:%S")=='00:10:00'):
        if True:
            class ImageViewer:
                def __init__(self, root, title, folder_path, column):
                    self.root = root
                    self.title = title
                    self.folder_path = folder_path
                    self.column = column

                    self.images = []
                    self.current_index = 0

                    self.setup_ui()

                    if os.path.exists(self.folder_path):
                        self.setup_observer()
                        self.update_image()
                    else:
                        self.name_label.config(text='Carpeta no disponible', font=('Arial', 20))
                        self.label.config(image="")

                def setup_ui(self):
                    self.frame = tk.Frame(self.root)
                    self.frame.grid(row=0, column=self.column, padx=10, pady=10)

                    self.name_title = tk.Label(self.frame, text=self.title, font=('Arial', 20))
                    self.name_title.grid(row=0, column=0, columnspan=2)

                    self.name_label = tk.Label(self.frame, text='', font=('Arial', 14))
                    self.name_label.grid(row=1, column=0, columnspan=2)

                    self.label = tk.Label(self.frame)
                    self.label.grid(row=2, column=0, columnspan=2)

                def setup_observer(self):
                    self.event_handler = FileSystemEventHandler()
                    self.event_handler.on_created = self.on_created
                    self.event_handler.on_deleted = self.on_deleted
                    self.observer = Observer()
                    self.observer.schedule(self.event_handler, self.folder_path, recursive=False)
                    self.observer.start()

                def on_created(self, event):
                    self.images = self.get_sorted_images()

                def on_deleted(self, event):
                    self.images = self.get_sorted_images()

                def get_sorted_images(self):
                    images = [f for f in os.listdir(self.folder_path) if f.endswith('.png')]
                    return sorted(images)

                def show_image(self, image_path):
                    if os.path.exists(image_path):  
                        img = Image.open(image_path)
                        img = img.resize((450, 500))
                        img_tk = ImageTk.PhotoImage(img)
                        return img_tk
                    return None

                def update_image(self):
                    self.images = self.get_sorted_images()
                    if self.images:
                        if self.current_index >= len(self.images):
                            self.current_index = 0
                        img_path = os.path.join(self.folder_path, self.images[self.current_index])
                        img_tk = self.show_image(img_path)
                        if img_tk:
                            self.label.config(image=img_tk)
                            self.label.image = img_tk
                            image_name = self.images[self.current_index]
                            new_string = image_name.replace('goes16_', '').replace('_TrueColor', '')
                            new_string2 = new_string.replace('_', '-')
                            new_string3 = f'{new_string2[:10]} {new_string2[11:-4]}'
                            self.name_label.config(text=new_string3)
                        self.current_index += 1
                    else:
                        self.name_label.config(text='No hay imágenes', font=('Arial', 20))
                        self.label.config(image="")
                    self.root.after(2000, self.update_image) # tiempo entre imagenes

            def set_background_color(widget, color):
                widget.configure(background=color)

            def actualizar():
                actualizar1()
                actualizar2()
                actualizar3()
                actualizar4()

                root.after(600000, actualizar) # tiempo de actualizacion 

            def actualizar1():
                global texto1, fecha1
                #texto1, fecha1 = recibir_bot1()
                texto1, fecha1 = recibir("producto_uno")
                text_fecha1.delete("1.0", tk.END)
                text_fecha1.insert(tk.END, fecha1)

                text_texto1.delete("1.0", tk.END) 
                text_texto1.insert(tk.END, texto1)

            def actualizar2():
                global texto2, fecha2
                #texto2, fecha2 = recibir_bot2()
                texto2, fecha2 = recibir("producto_dos") 
                text_fecha2.delete("1.0", tk.END)
                text_fecha2.insert(tk.END, fecha2)

                text_texto2.delete("1.0", tk.END) 
                text_texto2.insert(tk.END, texto2)

            def actualizar3():
                global texto3, fecha3
                texto3, fecha3 = recibir("producto_tres")  
                text_fecha3.delete("1.0", tk.END)
                text_fecha3.insert(tk.END, fecha3)

                text_texto3.delete("1.0", tk.END) 
                text_texto3.insert(tk.END, texto3)

            def actualizar4():
                global texto4, fecha4
                texto4, fecha4 = recibir("producto_cuatro")  
                text_fecha4.delete("1.0", tk.END)
                text_fecha4.insert(tk.END, fecha4)

                text_texto4.delete("1.0", tk.END) 
                text_texto4.insert(tk.END, texto4)

            root = tk.Tk()
            root.title("Software - EATA")
            root.geometry("1900x1000")

            # Utilizar grid 
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            viewer1 = ImageViewer(root, 'Estimador de precipitación', 'G:/Otros ordenadores/PC JUAN/type1/', 0)
            viewer2 = ImageViewer(root, 'Incremento de vapor de agua', 'G:/Otros ordenadores/PC JUAN/type2/', 1)
            viewer3 = ImageViewer(root, 'Altura de la base de la nube', 'G:/Otros ordenadores\PC ELMER/type3/', 2)
            viewer4 = ImageViewer(root, 'Capas de nieve/nubes', 'G:/Otros ordenadores\PC ELMER/type4/', 3)

            fecha1 = "" 
            texto1 = ""
            fecha2 = ""
            texto2 = ""
            fecha3 = "" 
            texto3 = ""
            fecha4 = ""
            texto4 = ""

            # Usar Text en lugar de Label
            text_fecha1 = tk.Text(root, width=45, height=1) 
            text_fecha1.grid(row=3, column=0, sticky="ew")
            text_fecha2 = tk.Text(root, width=45, height=1) 
            text_fecha2.grid(row=3, column=1, sticky="ew")
            text_fecha3 = tk.Text(root, width=45, height=1) 
            text_fecha3.grid(row=3, column=2, sticky="ew")
            text_fecha4 = tk.Text(root, width=15, height=1) 
            text_fecha4.grid(row=3, column=3, sticky="ew")

            text_texto1 = tk.Text(root, width=45, height=15)
            text_texto1.grid(row=4, column=0, sticky="ew")
            text_texto2 = tk.Text(root, width=45, height=15)
            text_texto2.grid(row=4, column=1, sticky="ew")
            text_texto3 = tk.Text(root, width=45, height=15)
            text_texto3.grid(row=4, column=2, sticky="ew")
            text_texto4 = tk.Text(root, width=45, height=15)
            text_texto4.grid(row=4, column=3, sticky="ew")

            def set_background_color(widget, color):
                widget.configure(background=color)

            set_background_color(root, "white")

            actualizar()  # Llamar una vez al inicio para iniciar el ciclo de actualización

            root.mainloop()


    except Exception as e:
        print("error",e)


