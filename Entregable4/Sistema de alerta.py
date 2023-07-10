# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:43:34 2023

@author: Lucas
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np

img = cv2.imread('peru_contorno.png')

# Convertir la imagen a espacio de color HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir rangos de color para el blanco y el verde en el espacio de color HSV
green_lower = np.array([50, 30, 30])
green_upper = np.array([70, 255, 255])

# Crear máscaras para los rangos de color
green_mask = cv2.inRange(hsv, green_lower, green_upper)

# Aplicar la máscara a la imagen original para filtrar los colores
filtered = cv2.bitwise_and(img, img, mask=green_mask)
filtered[400:445, 0:50] = 0 #Eliminar logo del producto

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
plt.imshow(thresh)




