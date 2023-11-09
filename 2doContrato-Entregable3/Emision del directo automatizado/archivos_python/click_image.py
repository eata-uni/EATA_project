import pyautogui

def detener_transmision():
    image_location = pyautogui.locateOnScreen('images/detener_transmision.png')
    if image_location:
        x, y = pyautogui.center(image_location)
        pyautogui.click(x, y)
    else:
        print("La imagen no se encontró en la pantalla.")

def equis():
    image_location = pyautogui.locateOnScreen('images/equis.png')
    if image_location:
        x, y = pyautogui.center(image_location)
        pyautogui.click(x, y)
    else:
        print("La imagen no se encontró en la pantalla.")


def cerrar():
    image_location = pyautogui.locateOnScreen('images/cerrar.png')
    if image_location:
        x, y = pyautogui.center(image_location)
        pyautogui.click(x, y)
    else:
        print("La imagen no se encontró en la pantalla.")

def terminar_emision():
    image_location = pyautogui.locateOnScreen('images/terminar_emision.png')
    if image_location:
        x, y = pyautogui.center(image_location)
        pyautogui.click(x, y)
    else:
        print("La imagen no se encontró en la pantalla.")
        

