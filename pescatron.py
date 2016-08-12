import cv2
import numpy as np
import autopy

image = autopy.bitmap.capture_screen()
image = image.get_portion([660, 200], [600, 300])
h = image.height
w = image.width
imgtest = np.zeros((h,w,3), np.uint8)
cv2.namedWindow("image")
c = 0

lower_red = np.array([13,50,50])
upper_red = np.array([167,255,255])

estado = 'inicio'

while (1):

    c = c+1

    image = autopy.bitmap.capture_screen()
    image = image.get_portion([660, 200], [600, 300])
    nombre = 'imagen'+'.png'
    image.save(nombre)
    img = cv2.imread('imagen.png')
    cv2.imshow("image", img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    mask2 = cv2.bitwise_not(mask)
    cv2.imshow("image3", mask2)

    # print mask2

    if c == 1 and estado == 'inicio':
        img2 = mask2
        print "Iniciando... 3 segundos..."
        estado = 'lanzar'
        cv2.waitKey(3000)
        autopy.mouse.move(660+600, 200+300)

    resta = mask2-img2

    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(resta,kernel,iterations = 1)

    cv2.imshow("erosion", erosion)

    img2 = mask2

    if sum(sum(erosion)) >= 2000:

        if estado == 'salvacords':

            repe = 0
            indexf = 300
            indexc = 150
            for indexc in range(len(resta)) :
                for indexf, item in enumerate(resta[indexc]):
                    if item == 255:
                        repe = repe + 1
                    else:
                        repe = 0

                    if repe >= 5:
                        posx = 660+indexf
                        posy = 200+indexc
                        break
                if repe >= 5:
                    break

            print "Salvando posicion en ", posx, posy
            esperando = 0
            estado = 'esperando'

        if estado == 'hanpicado':
            autopy.mouse.move(posx, posy)
            cv2.waitKey(20)
            autopy.mouse.click(autopy.mouse.RIGHT_BUTTON)
            print "Pilla pilla en posicion guardada"
            delay = 0
            estado = 'fin'

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
            autopy.mouse.move(660+600, 200+300)
        if delay >= 20:
            estado = 'lanzar'

    cv2.waitKey(50)

