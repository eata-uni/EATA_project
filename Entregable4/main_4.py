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
path_driver = r"C:\Users\Lucas\Desktop\project_EATA_Lucas\driver_chrome\chromedriver.exe"

origen = r'C:\Users\Lucas\Downloads'
destino = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\Database' #almacaenar imagenes descaragdas
destino_hydro = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\Database_hydro'

#mascaras de los departamentos
ruta_departamentos_mask = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\mask_dep'

#mascaras generadas por la intersecccion
ruta_clouds_mask = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\clouds_mask'
ruta_precipitation_mask= r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\precipitation_mask'

informe_cloud = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\Informe_cloud'
informe_hydro = r'C:\Users\Lucas\project_EATA_Lucas\Entregable4\Informe_hydro'

#Ingrese el tiempo de espera
wait_time = 10 #son 10 min

#Tiempo para acabar la ejecucion del programa
stop_time = 40000000

treshold = 10

cont_time = 0
bool_stop = True
aux_bool = True


try:
    
    
    while bool_stop:
        driver = tool_ETA.begin_url(path_driver, url)
        
        if aux_bool:
            
            tool_ETA.dowload_product(driver, origen, destino, product = 'cloud')
            tool_ETA.deteccion_cloud(destino , ruta_clouds_mask, ruta_departamentos_mask, informe_cloud, treshold)
            driver.close()
            
            
            driver = tool_ETA.begin_url(path_driver, url)
            tool_ETA.dowload_product(driver, origen, destino_hydro, product = 'hydro')
            tool_ETA.deteccion_precipitation(destino_hydro , ruta_precipitation_mask, ruta_departamentos_mask, informe_hydro, treshold)
            driver.close()
        
            
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
            
            tool_ETA.dowload_product(driver, origen, destino, product = 'cloud')
            tool_ETA.deteccion_cloud(destino , ruta_clouds_mask, ruta_departamentos_mask, informe_cloud, treshold)
            driver.close()
            
            
            driver = tool_ETA.begin_url(path_driver, url)
            tool_ETA.dowload_product(driver, origen, destino_hydro, product = 'hydro')
            tool_ETA.deteccion_precipitation(destino_hydro , ruta_precipitation_mask, ruta_departamentos_mask, informe_hydro, treshold)
            driver.close()
            
        
        aux_bool = False


except NoSuchElementException:
    print("Hubo un error")




