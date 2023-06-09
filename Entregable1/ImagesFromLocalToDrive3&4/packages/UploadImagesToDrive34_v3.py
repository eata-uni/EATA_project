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
            


def check_newImage_3():
    from login import start_login
    from check_newDownloadedImage import start_check_3
    import time
    while True:
        try:
            start_login()
            start_check_3()
            time.sleep(5)
            print("Se ejecuto check_newImage")
        except Exception as error:
            print(f'Se produjo un error eh check: {error}')
            time.sleep(30)
            continue
        
def check_newImage_4():
    from login import start_login
    from check_newDownloadedImage import start_check_4
    import time
    while True:
        try:
            start_login()
            start_check_4()
            time.sleep(5)
            print("Se ejecuto check_newImage")
        except Exception as error:
            print(f'Se produjo un error eh check: {error}')
            time.sleep(30)
            continue
            
def delete_3():
    import time
    from delete import start_delete_3
    while True:
        try:
            start_delete_3()
            time.sleep(10)
            print("Seejecuto delete")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue
        
def delete_4():
    import time
    from delete import start_delete_4
    while True:
        try:
            start_delete_4()
            time.sleep(10)
            print("Seejecuto delete")
        except Exception as error:
            print(f'Se produjo un error en delete: {error}')
            time.sleep(30)
            continue
        
aut = threading.Thread(target=auth)
check_3 = threading.Thread(target=check_newImage_3)
check_4 = threading.Thread(target=check_newImage_4)
dele_3 = threading.Thread(target=delete_3)
dele_4 = threading.Thread(target=delete_4)

aut.start()
check_3.start()
check_4.start()
dele_3.start()
dele_4.start()
