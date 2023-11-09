import pygetwindow as gw
import pyautogui

def cerrar_obs():
    # Encuentra la ventana de OBS minimizada en la barra de herramientas
    obs_window = gw.getWindowsWithTitle("OBS 29.1.3")[0]

    # Cierra la ventana de OBS
    obs_window.close()

