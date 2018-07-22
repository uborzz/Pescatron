import cv2
import numpy as np
# import autopy
# from time import sleep
# from PIL import Image
import pyautogui
# from Tkinter import *

## Pruebas config para capturar solamente la zona de interes y no toda imagen+recorte
## Pruebas captura toda imagen y escalado

# autopy_image = autopy.bitmap.capture_screen(((660+offset, 200), (600, 300))) # <- old equivalente a recorte
# pyauto_pil_image = pyautogui.screenshot(region=(400, 400, 300, 400)) # Formato xi, yi, w, h? - 0,0 (origen) ARRIBA-IZQ
image = pyautogui.screenshot()  # PIL Image
image = np.array(image)  # Pil image -> pasada a numpy array -> (ocv)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # swap canales rojo-azul
image = cv2.resize(image, None, fx=0.75, fy=0.75)  # scale al 75%

cv2.imshow("screen miniature", image)  # muestra imagen

cv2.waitKey(0)
