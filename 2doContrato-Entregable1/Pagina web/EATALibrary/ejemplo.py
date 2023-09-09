from comentarios import enviar
from imagen import subir, eliminar

# Para el Perú
enviar("producto_uno","Comentario")
enviar("producto_dos","Comentario")
enviar("producto_tres","Comentario")
enviar("producto_cuatro","Comentario")

# Por Departamentos
enviar("producto_uno_Lima","Comentario")
enviar("producto_dos_Lima","Comentario")
enviar("producto_tres_Lima","Comentario")
enviar("producto_cuatro_Lima","Comentario")

nombre_archivo = "2023-09-05 18-17-00.jpg" # nombre con el cual se subirá en el storage
ruta_local = ruta_local = "C:/Users/.../2023-09-05 18-17-00.jpg" 
tipo = "TypeN" # TypeN es una carpeta dentro del storage

subir(nombre_archivo, ruta_local, tipo) # sube una imagen
eliminar('Images/TypeN/') # elimina todas las imagenes dentro de la carpeta TypeN
