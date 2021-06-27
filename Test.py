from PIL.ImageOps import grayscale
import pyautogui
import pydirectinput
import time

import cv2 as cv
import numpy as np

METINTEXTDISTANCE = 40
healtbarrgbcolor = (102,51,51) #rgb

healthbarnotempty = False
pickupkeypressed = False
healthbar_located = False
pixelcolor = (0, 0, 0)

class Metin:

    def locateHealthBar():
        healthbarlocation = pyautogui.locateOnScreen('E:\Python\\autogui\\images\\bar_full.png', confidence=0.9, grayscale=True)

        if healthbarlocation:
            print("Healthbarposition located: " + str(healthbarlocation))
            return healthbarlocation

    
    def checkIfMetinStillAlive(healthbarlocation):
        leftouterpixellocation_x = int(healthbarlocation.left + 14)
        leftouterpixellocation_y = int(healthbarlocation.top + 3)

        # Try to get the Pixel-Color
        checkedColor = False
        pixelcolor = (0, 0, 0)
        
        try:
            pixelcolor = pyautogui.pixel(leftouterpixellocation_x, leftouterpixellocation_y)
            checkedColor = True
        except Exception:
            print("Error")
            return True

        if pixelcolor == (99, 39, 39):
            return True

        elif checkedColor:
            print('Pixelcolor: ' + str(pixelcolor))
            return False

    def collectLoot():
        print('collecting loot')
        time.sleep(0.5)
        pydirectinput.press('z', 3, interval=0.1) #cause of us layout


    def findMetinOpenCV():
        screenshot = np.array(pyautogui.screenshot()) 
        img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        template = cv.imread('E:\Python\\autogui\\metin_writing.png',0)
        w, h = template.shape[::-1]

        res = cv.matchTemplate(img_gray,template,cv.TM_CCORR_NORMED)
        threshold = 0.85
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            print(f'Metin found at {pt[0] + w} and {pt[1] + h + METINTEXTDISTANCE}')
            pyautogui.moveTo(pt[0] + w, pt[1] + h + METINTEXTDISTANCE, 0.2)
            pyautogui.click(clicks=2, interval=0.1)

            return True
            # cv.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            # cv.imwrite('res.png',img_gray)

        print('No Metin found')
        
    def lookaround():
        print('looking around')
        pydirectinput.keyDown('numpad4')
        pydirectinput.keyDown('left')
        time.sleep(1)
        pydirectinput.keyUp('numpad4')
        pydirectinput.keyUp('left')

    
def run_bot():
    # Locate the Healthbar for init
    healthbarlocation = 0
    while not healthbarlocation:
        healthbarlocation = Metin.locateHealthBar()

    while healthbarlocation:
        # try to find a metin:
        if Metin.findMetinOpenCV():
            # check if the metin is still alive
            while Metin.checkIfMetinStillAlive(healthbarlocation):
                time.sleep(1)

            Metin.collectLoot()

        else:
            time.sleep(2)
            Metin.lookaround()


if __name__ == '__main__':
    run_bot()

# while True:
#     if not Metin.findMetinOpenCV():
#         time.sleep(3)
#     else:

#         healthbarlocation = pyautogui.locateOnScreen('E:\Python\\autogui\\bar_full.png', confidence=0.9, grayscale=True)

#         if healthbarlocation:
#             print("Healthbarposition located: " + str(healthbarlocation))
#             healthbar_located = True
#             leftouterpixellocation_x = int(healthbarlocation.left + 14)
#             leftouterpixellocation_y = int(healthbarlocation.top + 3)

#         while healthbar_located:
#             #pyautogui.screenshot("testshot.png", region=(healthbarlocation))

#             # Try to get the Pixel-Color
#             try:
#                 pixelcolor = pyautogui.pixel(leftouterpixellocation_x, leftouterpixellocation_y)
#             except:
#                 print("Error")

#             # If the Color is 99,39,39 the Healthbar isnt empty
#             if pixelcolor == (99, 39, 39):
#                 pickupkeypressed = False

#             else:
#                 if not pickupkeypressed :
#                     print("press y")
#                     time.sleep(0.5)
#                     pydirectinput.press('z') #cause of us layout
#                     pickupkeypressed = True

#             time.sleep(1)



        # time.sleep(1)

