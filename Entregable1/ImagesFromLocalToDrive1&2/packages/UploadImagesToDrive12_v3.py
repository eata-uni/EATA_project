# primero ejecutar start_auth() en auth.py
import threading

    
def auth():
    import time
    from auth import start_auth
    while True:
        try:
            start_auth()
            time.sleep(600)
        except Exception as error:
            print(f'Se produjo un error en auth: {error}')
            time.sleep(30)
            continue
            


def check_newImage_1():
    from login import start_login
    from check_newDownloadedImage import start_check_1
    import time
    while True:
        try:
            start_login()
            start_check_1()
            time.sleep(5)
            print("Se ejecuto check_newImage 1")
        except Exception as error:
            print(f'Se produjo un error eh check: {error}')
            time.sleep(30)
            continue
        
def check_newImage_2():
    from login import start_login
    from check_newDownloadedImage import start_check_2
    import time
    while True:
        try:
            start_login()
            start_check_2()
            time.sleep(5)
            print("Se ejecuto check_newImage 2")
        except Exception as error:
            print(f'Se produjo un error eh check: {error}')
            time.sleep(30)
            continue

def giftopng_1():
    import time
    from gif_to_png import start_giftopng_1
    while True:
        try:
            start_giftopng_1()
            time.sleep(2)
            print("Se ejecuto giftopng 1")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue   

def giftopng_2():
    import time
    from gif_to_png import start_giftopng_2
    while True:
        try:
            start_giftopng_2()
            time.sleep(2)
            print("Se ejecuto giftopng 2")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue      

def delete_1():
    import time
    from delete import start_delete_1
    while True:
        try:
            start_delete_1()
            time.sleep(10)
            print("Se ejecuto delete 1")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue
        
def delete_2():
    import time
    from delete import start_delete_2
    while True:
        try:
            start_delete_2()
            time.sleep(10)
            print("Se ejecuto delete 2")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue


aut = threading.Thread(target=auth)
check_1 = threading.Thread(target=check_newImage_1)
check_2 = threading.Thread(target=check_newImage_2)
gtp_1 = threading.Thread(target=giftopng_1)
gtp_2 = threading.Thread(target=giftopng_2)
dele_1 = threading.Thread(target=delete_1)
dele_2 = threading.Thread(target=delete_2)


aut.start()
check_1.start()
check_2.start()
gtp_1 .start()
gtp_2.start() 
dele_1.start()
dele_2.start()
