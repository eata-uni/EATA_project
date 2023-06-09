import threading
import time
from packages import auth
from packages import check_newUploadedImage
from packages import copy 
from packages import delete_before
from packages import make_file
import datetime
def const_auth():
    while True:
        try:
            auth.start()
            time.sleep(600)
        except Exception as e:
            print(f"Ha ocurrido un error en const_auth: {e}")
            continue

def make_files():
    try:
        make_file.for_downloads()
        make_file.for_interface()
    except Exception as e:
        print(f"Ha ocurrido un error en make_files : {e}")
        pass   

def get_images():
    try:
        check_newUploadedImage.start()
    except Exception as e:
        print(f"Ha ocurrido un error en get_images : {e}")   

def copy_images():
    try:
        copy.start_global()
    except Exception as e:
        print(f"Ha ocurrido un error en copy_images : {e}")   

def delete():
    while True:
        try:
            now = datetime.datetime.now()
            if now.hour >= 3:
                delete_before.start_global()
            time.sleep(1)
        except Exception as e:
            print(f"Ha ocurrido un error en delete: {e}")
            continue


cns_auth = threading.Thread(target = const_auth)
make_fls = threading.Thread(target = make_files)
get= threading.Thread(target=get_images)
cop = threading.Thread(target = copy_images)
dele = threading.Thread(target = delete)


cns_auth.start()
make_fls.start()
time.sleep(2)
get.start()     # se ejecuta 2s despues de make_fls
time.sleep(5)   
cop.start()     
time.sleep(5)
dele.start()

