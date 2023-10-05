from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from funciones import start_bloquear, saber_coordenadas, arrastrar
from funciones import click_queestaspensando, click_publicar, click_foto, click_anadirfoto
from funciones import click_user
from funciones import teclear, teclear_enter, copiar_pegar
from funciones import obtener_informacion, click_izquierdo
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/")

email = driver.find_element(by="xpath", value='//*[@id="email"]')
email.send_keys("eata.peru@uni.edu.pe")
time.sleep(1)
password = driver.find_element(by="xpath", value='//*[@id="pass"]')
password.send_keys("LuisAlejandro888")

password.send_keys(Keys.ENTER)

time.sleep(3)
driver.get("https://www.facebook.com/profile.php?id=100092441334414")
time.sleep(5)
#start_bloquear()
click_izquierdo(475,219)


time.sleep(1)
arrastrar(1277, 302, 1276, 358, 1)

time.sleep(0.5)
click_izquierdo(700, 750)

time.sleep(2)


archivo, contenido = obtener_informacion()
teclear(contenido)

click_izquierdo(653, 737)
time.sleep(2)
click_izquierdo(642, 584)
time.sleep(5)
click_izquierdo(518, 65)
time.sleep(2)

copiar_pegar("C:/Users\Luis Chanquetti/Documents/Personal Projects/publicacion_automatizada/type1")

teclear_enter()
time.sleep(1)

click_izquierdo(253, 189)
teclear_enter()

time.sleep(1)
click_izquierdo(809, 518)

time.sleep(1)
click_izquierdo(635, 895)

time.sleep(10)
driver.quit()  # Cierra el navegador

