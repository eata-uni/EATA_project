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
import cv2
import numpy as np
import matplotlib.pyplot as plt


def mover_imagenes(origen, destino):
    # Obtener una lista de todas las imágenes en la carpeta de origen
    imagenes = [f for f in os.listdir(origen) if os.path.isfile(os.path.join(origen, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Iterar sobre cada imagen y moverla a la carpeta de destino
    for imagen in imagenes:
        # Generar el nuevo nombre de la imagen en caso de que ya exista en la carpeta de destino
        nombre_base, extension = os.path.splitext(imagen)
        nuevo_nombre = imagen
        contador = 1
        while os.path.exists(os.path.join(destino, nuevo_nombre)):
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            contador += 1
    
        # Mover la imagen a la carpeta de destino con el nuevo nombre (si es necesario)
        shutil.move(os.path.join(origen, imagen), os.path.join(destino, nuevo_nombre))


def dowload_image(driver):
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_UI_tools']/button[4]")
    elemento.click()
    time.sleep(20)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_downloadLink']")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/button")
    elemento.click()
    time.sleep(1)
    

    
def load_image(driver):
    elemento = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/button")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_productsCurrent']/ul/li[2]/div/div[1]/span[1]")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_productsCurrent']/ul/li/div/div[1]/span[1]")
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.CSS_SELECTOR, 'li#RE_button_products_all')
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.CSS_SELECTOR, 'h3#ui-accordion-RE_categories-header-22')
    elemento.click()
    time.sleep(1)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='ui-accordion-RE_categories-panel-22']/div[10]/div[1]/span[1]")
    elemento.click()
    time.sleep(1)

def move_display(driver):
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    ActionChains(driver).click_and_hold(elemento).perform()
    # Mover el cursor hacia abajo para arrastrar el elemento
    ActionChains(driver).move_by_offset(-200, -420).perform()
    ActionChains(driver).release(elemento).perform()
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]/div[2]/div[4]/div[2]/a[1]")
    elemento.click()
    time.sleep(2)
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    ActionChains(driver).click_and_hold(elemento).perform()
    #ActionChains(driver).move_by_offset(-100, -530).perform()
    ActionChains(driver).move_by_offset(-20, -50).perform()
    ActionChains(driver).release(elemento).perform()
    
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]/div[2]/div[4]/div[2]/a[1]")
    elemento.click()
    time.sleep(2)
    elemento = driver.find_element(By.XPATH,"//*[@id='RE_display']/div[1]/div[2]")
    
    ActionChains(driver).click_and_hold(elemento).perform()
    #ActionChains(driver).move_by_offset(-100, -530).perform()
    ActionChains(driver).move_by_offset(-50, -430).perform()
    ActionChains(driver).release(elemento).perform()
    time.sleep(5)
    

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


def ordenar_archivo(path):
    elementos = os.listdir(path)
    elementos_ordenados = sorted(elementos)
    elemento_mayor = max(elementos_ordenados, key=lambda x: int(''.join(filter(str.isdigit, x))))
    return elemento_mayor


def generator_cloud_mask(ruta_origen, ruta_destino):
    name_img = ordenar_archivo(ruta_origen)
    ruta_name = os.path.join(ruta_origen, name_img)
    
    img = cv2.imread(ruta_name)

    cloud_mask = extractor_clouds(img)
    cloud_mask_aux = cloud_mask.copy()
    cloud_mask = cv2.cvtColor(cloud_mask, cv2.COLOR_GRAY2RGB)
    
    cv2.imwrite(os.path.join(ruta_destino, name_img), cloud_mask)

    return cloud_mask_aux , img


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
        
        # Dibujar el contorno de la imagen en rojo
        imagen_rgb = cv2.drawContours(imagen_rgb, resultado['contorno_img'], -1, (0, 0, 255), 2)
        
        # Dibujar el contorno de la intersección en fucsia
        imagen_rgb = cv2.drawContours(imagen_rgb, resultado['contorno_inter'], -1, (255, 0, 255), 2)
        
        # Etiquetar la región roja con el nombre de la imagen
        font = cv2.FONT_HERSHEY_SIMPLEX
        M = cv2.moments(resultado['contorno_img'][0])
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        cv2.putText(imagen_rgb, nombre, (x, y), font, 1, (0, 0, 255), 2)
    
    return imagen_rgb