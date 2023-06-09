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