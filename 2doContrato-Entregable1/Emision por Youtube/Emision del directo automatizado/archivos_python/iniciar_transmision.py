import pyautogui
import time
import datetime

while True:
    try:
        # Obtener la hora actual
        hora_actual = datetime.datetime.now().time()
        if(hora_actual.strftime("%H:%M:%S")=='00:10:00'):
            def saber_coordenadas():
                time.sleep(5)
                current_position = pyautogui.position()
                print("Coordenadas actuales:", current_position)
                
            def click_mas():
                pyautogui.click(515, 857)

            def click_captura_de_ventana():
                pyautogui.click(629, 515)

            def click_aceptar():
                pyautogui.click(984, 647)

            def click_aceptar2():
                pyautogui.click(1155, 788)

            def click_navegador():
                pyautogui.click(753, 1065)
                

            def click_iniciar_transmision():
                pyautogui.click(1495, 784)


            time.sleep(15) # una vez abierto obs, despues de 5 seg se ejecutara esto:
            click_mas()
            time.sleep(2)
            click_captura_de_ventana()
            time.sleep(1)
            click_aceptar()
            time.sleep(1)
            click_aceptar2()
            time.sleep(1)
            click_iniciar_transmision()
            time.sleep(1)
            click_navegador()


    except Exception as e:
        print("error",e)


