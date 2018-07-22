import cv2
import numpy as np
import autopy

# ------- CONFIG --------------------

# -- Pesca en Lava/Agua
# lava = True
lava = False
#
# imshow_on = True
imshow_on = True

# -----------------------------------

offset = 0
image = autopy.bitmap.capture_screen()
image = image.get_portion([660+offset, 200], [600, 300])
h = image.height
w = image.width
imgtest = np.zeros((h, w, 3), np.uint8)

c = 0

# # general
# lower_red = np.array([13,50,50])
# upper_red = np.array([167,255,255])

# # nag
# lower_red = np.array([5,5,5])
# upper_red = np.array([175,b255,255])

# enhanced
lower_red_1 = np.array([168,65,65])  # Old 65<x<230
upper_red_1 = np.array([180,250,250])
lower_red_2 = np.array([0,65,65])
upper_red_2 = np.array([12,250,250])

# lava params
lower_blue = np.array([106,40,40])
upper_blue = np.array([131,253,253])

estado = 'inicio'
esperando = 0
wd = 0

while(1):

    c = c+1

    image = autopy.bitmap.capture_screen()
    image = image.get_portion([660+offset, 200], [600, 300])
    nombre = 'imagen'+'.png'
    image.save(nombre)
    img = cv2.imread('imagen.png')
    if imshow_on: cv2.imshow("capture", img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if lava == True:
        mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    else:
        mask2 = cv2.bitwise_or(cv2.inRange(hsv, lower_red_1, upper_red_1),cv2.inRange(hsv, lower_red_2, upper_red_2))


    if imshow_on: cv2.imshow("masked", mask2)

    if c == 1 and estado == 'inicio':
        img2 = mask2
        print "Iniciando... 3 segundos..."
        estado = 'lanzar'
        cv2.waitKey(3000)
        autopy.mouse.move(660+600+offset, 200+300)

    resta = mask2-img2 # old

    kernel = np.ones((3,3),np.uint8)   # OLD 3x3
    erosion = cv2.erode(resta,kernel,iterations = 1) # old
    # erosion = cv2.morphologyEx(resta,cv2.MORPH_OPEN,kernel) # erode + dilate

    if imshow_on: cv2.imshow("movement", erosion)

    img2 = mask2

    print estado, wd

    if sum(sum(erosion)) >= 2000:

        if estado == 'salvacords':
            wd = 0
            repe = 0
            indexf = 300
            indexc = 150
            for indexc in range(len(resta)) :
                for indexf, item in enumerate(resta[indexc]):
                    if item == 255:
                        repe = repe + 1
                    else:
                        repe = 0

                    if repe >= 4:
                        posx = 660+indexf+offset
                        posy = 200+indexc
                        break
                if repe >= 4:
                    break

            print "Salvando posicion en ", posx, posy
            esperando = 0
            estado = 'esperando'

        if estado == 'hanpicado':
            wd = 0
            autopy.mouse.move(posx, posy)
            cv2.waitKey(20)
            autopy.mouse.click(autopy.mouse.RIGHT_BUTTON)
            print "Pilla pilla en posicion guardada"
            delay = 0
            estado = 'fin'
    else:
        #watchdog
        if estado == 'hanpicado' or estado == 'salvacords':
            wd = wd + 1
            if wd >= 180:
                estado = 'lanzar'
                esperando = 0
                wd = 0

    if estado == 'esperando':
        esperando = esperando + 1
        if esperando >=  10:
            print 'esperando...'
            estado = 'hanpicado'


    if estado == 'lanzar':
        print "LANZAAAAAAAAAAAAA"
        autopy.mouse.click(autopy.mouse.CENTER_BUTTON)
        estado = 'salvacords'

    if estado == 'fin':
        print "esperando para lanzar"
        delay = delay + 1
        if delay == 10:
            autopy.mouse.move(660+offset+600, 200+300)
        if delay >= 20:
            estado = 'lanzar'

    cv2.waitKey(50)

