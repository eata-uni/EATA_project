# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:19:38 2023

@author: Lucas
"""
from selenium import webdriver
import os
import shutil
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime
import cv2
import numpy as np
from PIL import Image


def mover_imagenes(origen, destino):
    #cargando boundaries:
    ruta_boundaries = '{}/{}'.format('utils','mask_img.png')
    boundaries = cv2.imread(ruta_boundaries)
    new_boundaries = binarize_and_transform_cv(boundaries, threshold=240)
    
    # Obtener una lista de todas las imágenes en la carpeta de origen
    imagenes = [f for f in os.listdir(origen) if os.path.isfile(os.path.join(origen, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    
    # Iterar sobre cada imagen y moverla a la carpeta de destino
    for imagen in imagenes:
        # Generar el nuevo nombre de la imagen en caso de que ya exista en la carpeta de destino
        nombre_base, extension = os.path.splitext(imagen)
        
        #nuevo_nombre = imagen
        now = datetime.datetime.now()
        new_name = now.strftime('%Y-%m-%d %H-%M-%S')
        #nuevo_nombre = f"{new_name}{extension}"
        ruta_database = os.path.dirname(destino)
        if extension =='.gif':
            # abrir el archivo GIF con Pillow
            ruta_archivo_gif = os.path.join(origen, imagen)
            imagen_gif = Image.open(ruta_archivo_gif)
            
            # obtener la ruta de salida para el archivo PNG
            name_png = new_name+ '.png'
            
            
            ruta_archivo_png_cache = os.path.join(ruta_database, 'cache', name_png)
            borrar_y_crear_carpeta(os.path.join(ruta_database, 'cache'))
            imagen_gif.save(ruta_archivo_png_cache, 'PNG')
            # eliminar el archivo GIF
            imagen_gif.close()
            
            img = cv2.imread(ruta_archivo_png_cache)
                      
            ruta_data = tipo_img(img)
           
            new_destino = os.path.join(ruta_database, ruta_data)
            
            shutil.move(ruta_archivo_png_cache , os.path.join(new_destino, name_png))
            
            #colocando los boundaries de los departamentos
            new_img = multiply_images(img, new_boundaries)
            cv2.imwrite( os.path.join(new_destino, name_png), new_img)
           
            
            time.sleep(1)
            # intentar eliminar el archivo
            try:
                os.remove(ruta_archivo_gif)
                #print(f"Archivo {ruta_archivo_gif} eliminado con éxito.")
            except OSError as error:
                print(f"No se pudo eliminar el archivo {ruta_archivo_gif}: {error}")
        else:
            nuevo_nombre = f"{new_name}{extension}"
            
            
            img = cv2.imread(os.path.join(origen, imagen))
            ruta_data = tipo_img(img)
            new_destino = os.path.join(ruta_database, ruta_data)
            # Mover la imagen a la carpeta de destino con el nuevo nombre (si es necesario)
            shutil.move(os.path.join(origen, imagen), os.path.join(new_destino, nuevo_nombre))
            
            new_img = multiply_images(img, new_boundaries)
            cv2.imwrite( os.path.join(new_destino, nuevo_nombre), new_img)
            '''
            if np.mean(imagen[:,:,0]) and  
            if obtener_ultimo_elemento(destino) not in '_hydro':
                
            else:
            '''    
def borrar_y_crear_carpeta(ruta_carpeta):
    # Comprobar si la carpeta existe
    if os.path.exists(ruta_carpeta):
        # Eliminar la carpeta y su contenido
        shutil.rmtree(ruta_carpeta)
        # Crear la carpeta nuevamente
        os.makedirs(ruta_carpeta)
    else:
        
        # Crear la carpeta nuevamente
        os.makedirs(ruta_carpeta)
        
def tipo_img(img):
    B = np.mean(img[:,:,0])
    G = np.mean(img[:,:,1])
    R = np.mean(img[:,:,2])
    
    if B < 120 or G < 120 or R < 120:
        ruta_data = 'Database'
    else:
        ruta_data = 'Database_hydro'
    return ruta_data

def obtener_ultimo_elemento(string):
    elementos = string.split("\\")
    ultimo_elemento = elementos[-1]
    return ultimo_elemento
'''
def corregir_extension(nombre_archivo, origen):
    # Dividir la ruta de archivo en nombre y extensión
    nombre, extension = os.path.splitext(nombre_archivo)
    # Si la extensión contiene varios puntos, conservar solo la primera parte
    if "." in nombre:
        return nombre
    # Combinar el nombre y la extensión corregida en una sola cadena
    else:
        return nombre_archivo
'''

def dowload_image(driver):
    
    #Configuro para tiempo actual
    elemento = driver.find_element(By.XPATH,"//*[@id='ui-id-14']")
    elemento.click()
    time.sleep(1)


    elemento = driver.find_element(By.XPATH,"//*[@id='RE_timesRelative_from']/select/option")
    elemento.click()
    time.sleep(1)

    elemento = driver.find_element(By.XPATH,"//*[@id='RE_timesRelative']/button/span[2]")
    elemento.click()
    time.sleep(1)
    
    time.sleep(10)
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_UI_tools']/button[4]/span[2]")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='image_mode']/label[2]/span")
    elemento.click()
    time.sleep(10)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_downloadLink']")
    elemento.click()
    time.sleep(1)

def login(driver):
    id_usuario = 'SergioSosa'
    password = 'eata1234'
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_button_login']")
    elemento.click()
    time.sleep(1)
    
    
    elemento = driver.find_element(By.XPATH,"//*[@id='user_name']")
    elemento.send_keys(id_usuario)
    time.sleep(1)
    
    
    elemento = driver.find_element(By.XPATH,"//*[@id='user_pass']")
    elemento.send_keys(password)
    time.sleep(1)
    
    
    elemento = driver.find_element(By.XPATH,"//*[@id='login_user']/span[2]")
    elemento.click()
    time.sleep(1)
    
    
def load_image(driver, hydro = False):
    elemento = driver.find_element(By.CSS_SELECTOR, 'li#RE_button_products_all')
    elemento.click()
    time.sleep(1)
    
    if hydro:
        elemento = driver.find_element(By.XPATH, "//*[@id='ui-accordion-RE_categories-header-52']")
        elemento.click()
        time.sleep(3)
        
        elemento = driver.find_element(By.XPATH,"//*[@id='ui-accordion-RE_categories-panel-52']/div[1]/div[1]/span[1]")
        elemento.click()
        time.sleep(1)
        
    else:
        elemento = driver.find_element(By.CSS_SELECTOR, 'h3#ui-accordion-RE_categories-header-22')
        elemento.click()
        time.sleep(3)
        
        elemento = driver.find_element(By.XPATH,"//*[@id='ui-accordion-RE_categories-panel-22']/div[10]/div[1]/span[1]")
        elemento.click()
        time.sleep(1)

def move_display(driver):
    time.sleep(10)
    elemento = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/button")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_productsCurrent']/ul/li[2]/div/div[1]/span[1]")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_productsCurrent']/ul/li/div/div[1]/span[1]")
    elemento.click()
    
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    ActionChains(driver).click_and_hold(elemento).perform()
    # Mover el cursor hacia abajo para arrastrar el elemento
    ActionChains(driver).move_by_offset(-200, -420).perform()
    ActionChains(driver).release(elemento).perform()
    
    time.sleep(1)
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]/div[2]/div[4]/div[2]/a[1]")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    ActionChains(driver).click_and_hold(elemento).perform()
    #ActionChains(driver).move_by_offset(-100, -530).perform()
    ActionChains(driver).move_by_offset(-20, -50).perform()
    ActionChains(driver).release(elemento).perform()
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]/div[2]/div[4]/div[2]/a[1]")
    elemento.click()
    time.sleep(1)
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    
    ActionChains(driver).click_and_hold(elemento).perform()
    #ActionChains(driver).move_by_offset(-100, -530).perform()
    ActionChains(driver).move_by_offset(-50, -430).perform()
    ActionChains(driver).release(elemento).perform()
    time.sleep(1)
    
def dowload_product(driver, origen, destino, product = 'cloud'):
    #Reubica la imagen
    move_display(driver)
    #logearse en la pagina
    login(driver)
    
    #Carga la imagen con la pagina
    if product == 'cloud':
        load_image(driver)
    if product == 'hydro':
        load_image(driver, hydro = True)
        
    #descarga la imagen
    dowload_image(driver)
    time.sleep(20)
    #mueve la imagen descargada a a la ruta deseada
    mover_imagenes(origen, destino)
    

def begin_url(path_driver, url):
    # Inicializar el driver de Selenium
    driver = webdriver.Chrome(executable_path = path_driver )
    # Navegar a la página web deseada
    driver.get(url)
    
    return driver


'''
boundaries
'''
def binarize_and_transform_cv(img, threshold=240):
    # Cargamos la imagen
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Leemos en escala de grises

    # Binarizamos la imagen con el threshold proporcionado
    _, data = cv2.threshold(img, threshold, 1, cv2.THRESH_BINARY)

    # Creamos un array nuevo con la misma forma que data pero con 3 canales
    new_data = np.zeros((*data.shape, 3), dtype=np.uint8)
    
    # Asignamos [1,1,1] a los píxeles que eran mayores que threshold y [0,0,0] a los demás
    new_data[data == 1] = [1,1,1]
    new_data[data == 0] = [0,0,0]
    
    return new_data


def multiply_images(img1, img2):
    
    # Redimensionamos la segunda imagen al tamaño de la primera
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Multiplicamos las imágenes. Para evitar overflow, primero las convertimos a float32
    multiplied = cv2.multiply(img1.astype(float), img2_resized.astype(float))

    # Normalizamos los valores al rango original [0,255]
    normalized = cv2.normalize(multiplied, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return normalized



'''
Esta parte estan las funciones apra la deteccion de nubes y activar la alarma
'''

def extractor_clouds(img):

    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Definir rangos de color para el blanco y el verde en el espacio de color HSV
    green_lower = np.array([50, 30, 30])
    green_upper = np.array([70, 255, 255])

    # Crear máscaras para los rangos de color
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Aplicar la máscara a la imagen original para filtrar los colores
    filtered = cv2.bitwise_and(img, img, mask=green_mask)
    filtered[400:445, 0:50] = 0 #Eliminar logo del producto

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    _, mask_final = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    
    return mask_final

'''

def ordenar_archivo(path):
    elementos = os.listdir(path)
    elementos_ordenados = sorted(elementos)
    elemento_mayor = max(elementos_ordenados, key=lambda x: int(''.join(filter(str.isdigit, x))))
    return elemento_mayor

'''
def ordenar_archivo(directorio):
    # Obtener la lista de archivos en el directorio
    lista_archivos = os.listdir(directorio)
    # Crear una lista de tuplas (nombre_archivo, tiempo_creacion)
    lista_tiempos_creacion = [(nombre_archivo, os.stat(os.path.join(directorio, nombre_archivo)).st_mtime) for nombre_archivo in lista_archivos]
    # Ordenar la lista por tiempo de creación en orden descendente
    lista_tiempos_creacion.sort(key=lambda x: x[1], reverse=True)
    # Devolver el nombre del archivo más reciente
    return lista_tiempos_creacion[0][0]


def generator_cloud_mask(ruta_origen, ruta_destino):
    
    name_img = ordenar_archivo(ruta_origen)
    ruta_name = os.path.join(ruta_origen, name_img)
    
    img = cv2.imread(ruta_name)

    cloud_mask = extractor_clouds(img)
    cloud_mask_aux = cloud_mask.copy()
    cloud_mask = cv2.cvtColor(cloud_mask, cv2.COLOR_GRAY2RGB)
    
    cv2.imwrite(os.path.join(ruta_destino, name_img), cloud_mask)

    return cloud_mask_aux , img, name_img


def buscar_imagenes_interseccion(carpeta, img_ref, threshold):
    """
    Calcula la intersección de pixeles entre las imágenes de la carpeta y una imagen de referencia.
    
    :param carpeta: la ruta de la carpeta que contiene las imágenes a procesar
    :param imagen_ref: la ruta de la imagen de referencia
    :param threshold: el valor umbral para considerar que hay intersección de pixeles
    :return: un diccionario con el contorno de la imagen, el contorno de la intersección y la cantidad de pixeles en la intersección
    """
    # Leer la imagen de referencia
   #img_ref = cv2.imread(imagen_ref, 0)  # 0 indica que se lee en escala de grises
    
    # Crear el diccionario que se va a retornar
    resultados = {}
    
    # Recorrer todas las imágenes de la carpeta
    for archivo in os.listdir(carpeta):
        # Leer la imagen y convertirla a escala de grises
        ruta = os.path.join(carpeta, archivo)
        img = cv2.imread(ruta, 0)
        
        # Comprobar si img y img_ref tienen el mismo tamaño
        if img.shape != img_ref.shape:
            # Si las dimensiones son diferentes, ajustar img al tamaño de img_ref
            img = cv2.resize(img, (img_ref.shape[1], img_ref.shape[0]))
            umbral, img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)

            
        # Calcular la intersección de pixeles entre la imagen y la imagen de referencia
        interseccion = cv2.bitwise_and(img, img_ref)
       
        
        # Calcular la cantidad de pixeles en la intersección
        cantidad_pixeles = cv2.countNonZero(interseccion)
        
        # Verificar si la cantidad de pixeles en la intersección es mayor al umbral
        if cantidad_pixeles > threshold:
            # Calcular el contorno de la imagen y de la intersección
            contorno_img, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contorno_inter, _ = cv2.findContours(interseccion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Agregar los resultados al diccionario
            resultados[archivo] = {
                'contorno_img': contorno_img,
                'contorno_inter': contorno_inter,
                'cantidad_pixeles': cantidad_pixeles
            }
    
    return resultados


def etiquetar_resultados(resultados, imagen_rgb):
    """
    Etiqueta una imagen con los resultados de la función 'calcular_interseccion_carpeta'.
    
    :param resultados: un diccionario con los resultados de la función 'calcular_interseccion_carpeta'
    :param imagen_rgb: una imagen en formato RGB (3 canales)
    :return: la imagen etiquetada
    """
    # Verificar si el diccionario de resultados está vacío
    if not resultados:
        print("No hay lluvias")
        return imagen_rgb
    
    # Etiquetar cada imagen en los resultados
    for ruta, resultado in resultados.items():
        # Obtener el nombre de la imagen sin la extensión
        nombre = os.path.splitext(os.path.basename(ruta))[0]
        
        # Dibujar el contorno del departamento
        imagen_rgb = cv2.drawContours(imagen_rgb, resultado['contorno_img'], -1, (0, 0, 255), 2)
        
        # Dibujar el contorno de las zonas con nubes de lluvia
        imagen_rgb = cv2.drawContours(imagen_rgb, resultado['contorno_inter'], -1, (255, 0, 255), 2)
        
        # Etiquetar la región roja con el nombre de la imagen
        '''
        font = cv2.FONT_HERSHEY_SIMPLEX
        M = cv2.moments(resultado['contorno_img'][0])
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        cv2.putText(imagen_rgb, nombre, (x, y), font, 1, (0, 0, 255), 2)
        '''
    
    return imagen_rgb

def deteccion(destino , ruta_clouds_mask, ruta_departamentos_mask, save_path, treshold):
    cloud_mask, imagen_rgb, name_img= generator_cloud_mask(destino, ruta_clouds_mask)
    #obtenemos departamentos con lluvia
    array_lluvia = buscar_imagenes_interseccion(ruta_departamentos_mask, cloud_mask, treshold)
    #obtenemos imagen con intersecciones localizadas
    new_img = etiquetar_resultados(array_lluvia, imagen_rgb)
    
    
    #Almacenamos 
    cv2.imwrite(os.path.join(save_path, '{}.png'.format(name_img)), new_img )
    
    
    
    
    
    
    