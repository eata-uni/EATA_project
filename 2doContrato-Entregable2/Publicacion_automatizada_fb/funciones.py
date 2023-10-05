# -*- coding: utf-8 -*-
from pynput.mouse import Button, Controller
import time
from screen_search import Search
import pyautogui
import pyperclip
import os

mouse = Controller()
def click_raton_posicion (x,y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
 
 
 
def imagen():
    search = Search("images/bloquear.png")
    pos = search.imagesearch()

    if pos[0] == -1:
        return False
    else:
        return pos
 
 
def start_bloquear():
    coordenadas = imagen()
    #si encuentro
    if coordenadas!= False:
        click_raton_posicion (coordenadas[0], coordenadas[1])



def saber_coordenadas():
    # Espera unos segundos para que tengas tiempo de mover el cursor al lugar adecuado
    time.sleep(5)

    # Obtiene las coordenadas actuales del cursor del mouse
    x, y = pyautogui.position()
    return x,y


def arrastrar(inicio_x, inicio_y, fin_x, fin_y, duracion_arrastre):
    # Realiza el clic y mantenlo presionado
    pyautogui.mouseDown(inicio_x, inicio_y)
    # Espera un breve período de tiempo antes de comenzar el arrastre
    time.sleep(1)
    # Simula el arrastre hacia las coordenadas finales
    pyautogui.moveTo(fin_x, fin_y, duration=duracion_arrastre)
    # Suelta el clic izquierdo para completar el arrastre
    pyautogui.mouseUp()

#saber_coordenadas()
def click_queestaspensando():
    ruta_imagen = 'images/queestaspensando.png'
    centro_imagen = pyautogui.locateCenterOnScreen(ruta_imagen)
    if centro_imagen is not None:
        pyautogui.click(centro_imagen)
    else:
        print("La imagen no se encontró en la pantalla.")

def click_publicar():
    ruta_imagen = 'images/publicar.png'
    centro_imagen = pyautogui.locateCenterOnScreen(ruta_imagen)
    if centro_imagen is not None:
        pyautogui.click(centro_imagen)
    else:
        print("La imagen no se encontró en la pantalla.")
        
def teclear(palabra):
    pyautogui.typewrite(palabra, interval=0.1)
    #pyperclip.copy("@")
    #pyautogui.hotkey("ctrl", "v")
def copiar_pegar(palabra):
    pyperclip.copy(palabra)
    pyautogui.hotkey("ctrl", "v")

def teclear_enter():
    pyautogui.press('enter')


def click_foto():
    ruta_imagen = 'images/foto.png'
    centro_imagen = pyautogui.locateCenterOnScreen(ruta_imagen)
    if centro_imagen is not None:
        pyautogui.click(centro_imagen)
    else:
        print("La imagen no se encontró en la pantalla.")

def click_anadirfoto():
    ruta_imagen = 'images/anadirfoto.png'
    centro_imagen = pyautogui.locateCenterOnScreen(ruta_imagen)
    if centro_imagen is not None:
        pyautogui.click(centro_imagen)
    else:
        print("La imagen no se encontró en la pantalla.")

def click_user():
    ruta_imagen = 'images/user.png'
    centro_imagen = pyautogui.locateCenterOnScreen(ruta_imagen)
    if centro_imagen is not None:
        pyautogui.click(centro_imagen)
    else:
        print("La imagen no se encontró en la pantalla.")

def obtener_informacion():
    # Ruta de la carpeta "info_type1"
    ruta_carpeta = "info_type1"  # Reemplaza con la ruta correcta

    try:
        # Lista todos los archivos en la carpeta "info_type1"
        archivos = os.listdir(ruta_carpeta)
        
        for archivo in archivos:
            # Combinar la ruta de la carpeta con el nombre del archivo
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            
            # Verificar si el elemento es un archivo
            if os.path.isfile(ruta_archivo):
                with open(ruta_archivo, "r", encoding="utf-8") as archivo_txt:
                    contenido = archivo_txt.read()
                    #print(f"Contenido de {archivo}:")
                    #print(contenido)
                    #print("\n")
                    return archivo, contenido
    except FileNotFoundError:
        print(f"La carpeta {ruta_carpeta} no se encuentra.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")


def click_izquierdo(x,y):
    coordenada_x = x
    coordenada_y = y
    pyautogui.click(x=coordenada_x, y=coordenada_y)


