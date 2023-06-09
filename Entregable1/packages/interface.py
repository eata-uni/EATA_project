
"""
import os
from PIL import Image, ImageTk
def get_image_files(folder):
    image_files = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            image_files.append(os.path.join(folder, filename))
    return image_files

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    return resized_image
"""
import os
from PIL import Image
import datetime

def get_image_files(folder):
    image_files = []
    current_date = datetime.datetime.now().date()
    
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            file_path = os.path.join(folder, filename)
            file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date()
            if file_date == current_date:
                image_files.append(file_path)
    
    return image_files

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    return resized_image
