import pygetwindow as gw
import pyautogui

def maximizar_chrome():
    # Encuentra la ventana de Chrome minimizada en la barra de herramientas
    chrome_window = gw.getWindowsWithTitle("Google Chrome")[0]

    # Enfoca la ventana minimizada
    chrome_window.restore()

    # Opcional: Puedes mover el mouse a la ventana para asegurarte de que está enfocada
    pyautogui.moveTo(chrome_window.left + 10, chrome_window.top + 10)

def minimizar_chrome():
    # Encuentra la ventana de Chrome
    chrome_window = gw.getWindowsWithTitle("Google Chrome")[0]

    # Minimiza la ventana
    chrome_window.minimize()

#maximizar_chrome()
