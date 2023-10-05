import datetime
import pyautogui
import time
from click_image import detener_transmision, equis
from abrir_chrome import maximizar_chrome
from cerrar_obs import cerrar_obs
import pygetwindow as gw

def saber_coordenadas():
    time.sleep(5)
    current_position = pyautogui.position()
    print("Coordenadas actuales:", current_position)
                

def click_terminar_transmision():
    pyautogui.click(1738, 138)

def click_finalizar():
    pyautogui.click(1634, 668)

def click_cerrar():
    pyautogui.click(1538, 933)

def click_der_captura_ventana():
    pyautogui.rightClick(515,780)

def click_eliminar():
    pyautogui.click(612,336)


def click_si():
    pyautogui.click(1046,548)

def click_der_cmd():
    pyautogui.rightClick(852,1060)

def click_cerrar_ventanas():
    pyautogui.click(849,1014)

def click_parte_obs():
    pyautogui.click(894,9)

                
def click_detener_transmision():
    pyautogui.click(1550,783)

def click_x():
    pyautogui.click(1891,7)

def click_cerrar():
    pyautogui.click(1501,942)

def click_minimizar():
    pyautogui.click(1781,18)


    
#saber_coordenadas()

time.sleep(600) # en tantos segundos despues de iniciado el directo, se finaliza
click_detener_transmision()
time.sleep(1)
click_der_captura_ventana()
time.sleep(1)
click_eliminar()
time.sleep(1)
click_si()
time.sleep(1)
maximizar_chrome()
time.sleep(90) #finaliza solo 
click_cerrar()
time.sleep(1)
cerrar_obs()
time.sleep(1)
# codigo para cerrar todos los codigos python
#click_der_cmd()
#time.sleep(1)
#click_cerrar_ventanas()



"""
#despues de abrir obs, despues de 120 seg se terminara la transmision 
click_terminar_transmision()
time.sleep(1)
click_finalizar()
time.sleep(1)
click_cerrar()
time.sleep(1)
click_der_captura_ventana()
time.sleep(1)
click_eliminar()
time.sleep(1)
click_si()
time.sleep(1)
click_parte_obs()
time.sleep(1)
print("Se esta apunto de detener la transmision")
time.sleep(1)
detener_transmision()
time.sleep(1)
equis()
time.sleep(1)
click_cerrar()
time.sleep(1)
click_minimizar()
#time.sleep(1)
#click_der_cmd()
#time.sleep(1)
#click_cerrar_ventanas()
"""


