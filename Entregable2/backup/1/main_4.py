# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import selenium
import pyautogui
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import tool_project_ETA as tool_ETA
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import cv2


url = "https://re.ssec.wisc.edu/?products=G16-ABI-FD-BAND02.100,G16-ABI-FD-BAND13.65&center=36.62792196407514,-94.74951171874999&zoom=4&width=949&height=776&timeproduct=G16-ABI-FD-BAND13&timespan=-6t&animationspeed=50&labels=lines"

origen = r'C:\Users\Lucas\Downloads'
destino = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\Database'

ruta_clouds_mask = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\clouds_mask'
ruta_departamentos_mask = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\mask_dep'
wait_time = 20
stop_time = 400
treshold = 50



cont_time = 0
bool_stop = True
aux_bool = True

try:
    
    while bool_stop:
        # Inicializar el driver de Selenium
        driver = webdriver.Chrome(executable_path = r"C:\Users\Lucas\project_EATA_Lucas\driver_chrome\chromedriver.exe" )
        
        # Navegar a la página web deseada
        driver.get(url)
        
        if aux_bool:
            time.sleep(10)
            #Carga la imagen con la pagina
            tool_ETA.load_image(driver)
            
            #Reubica la imagen
            
            tool_ETA.move_display(driver)
            tool_ETA.dowload_image(driver)
            tool_ETA.mover_imagenes(origen, destino)
            
            
        else:
            #Tiempo de carga
            with tqdm(total=wait_time) as pbar:
                for i in range(wait_time):
                   time.sleep(1)
                   pbar.update(1)
            
            if stop_time < cont_time:
                bool_stop = False
            else: 
                cont_time += wait_time
                
            #Carga la imagen con la pagina
            tool_ETA.load_image(driver)
            
            #Reubica la imagen
            tool_ETA.move_display(driver)
            tool_ETA.dowload_image(driver)
            
            #almacenamos la imagen en la base de datos
            tool_ETA.mover_imagenes(origen, destino)
        
        cloud_mask, imagen_rgb = tool_ETA.generator_cloud_mask(destino, ruta_clouds_mask)
        
        #obtenemos departamentos con lluvia
        array_lluvia = tool_ETA.buscar_imagenes_interseccion(ruta_departamentos_mask, cloud_mask, treshold)
        
        #obtenemos imagen con intersecciones localizadas
        new_img = tool_ETA.etiquetar_resultados(array_lluvia, imagen_rgb)
        
        #Almacenamos 
        cv2.imwrite('new_img.jpg',new_img )
        
        aux_bool = False
        
        #reactualizamos la pagina
        driver.close()
        
except NoSuchElementException:
    print("Hubo un error")

