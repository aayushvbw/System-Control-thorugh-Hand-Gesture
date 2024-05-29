import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui
import autopy
pyautogui.FAILSAFE = False    # if hand is non detectable then it will throw an error to overcome that error

from kitGesture import distance,R_Sq,get_swipe_direction
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

   
###  Camera panel and DPI(kind of)

wCam , hCam = 640,480
frameR = 150       # Frame Reduction
smoothening = 5


pTime = 0
plocX, plocY = 0, 0      # previous location of X and Y
clocX, clocY = 0, 0      # current location of X and Y

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()




devices = AudioUtilities.GetSpeakers()   # Get Output devices for audio
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0         # volume
volBar = 400    # Volume Bar
volPer = 0      # Percentage Volume


PATH=[]



while True:
    #1 find hand landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox, handtype = detector.findPosition(img)

    #2 getting tip of the fingers

    if len(lmList) != 0:
        x0, y0 = lmList[4][1:]          # thumb
        x1, y1 = lmList[8][1:]          # index
        x2, y2 = lmList[12][1:]         # middle
        x3, y3 = lmList[16][1:]         # Ring
        x4, y4 = lmList[20][1:]         # little





        # print(x1, y1, x2, y2)

        #3 check which fingers are up

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        length, img, lineInfo = detector.findDistance(8, 12, img)

        # if right hand is raised
        if handtype[0] == "Left":

            #4 only index finger and middle up : means : controling cursor

            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                # print(length)
                # print(length)
                if length < 32:

                    # 5 convert coordinates

                    xc = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    yc = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                    # 6 smoothen values  (better movement of cursor)

                    clocX = plocX + (xc - plocX) / smoothening
                    clocY = plocY + (yc - plocY) / smoothening

                    # 7 Move mouse
                    autopy.mouse.move(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY



            #8  clicking mode

            if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and length > 60:
                pyautogui.click(button = 'left', clicks = 1)
                pyautogui.sleep(0.25)

            if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
                pyautogui.click(button = 'right', clicks = 1)
                pyautogui.sleep(0.25)

            # slide show right
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
                pyautogui.press('right')
                pyautogui.sleep(0.25)
            # slide show left
            if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                pyautogui.press('left')
                pyautogui.sleep(0.25)

            # 9 Scroll Mode

             # down
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0 and length < 32:
                pyautogui.scroll(-80)
            # up
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                pyautogui.scroll(80)

            #10 Gestures (1. Volume ; 2. TaskBar Shifting)

            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(vol, [50, 300], [400, 150])
                volPer = np.interp(vol, [50, 300], [0, 100])
                print(int(length), vol)
                print(vol)
                volN = int(vol)
                if volN % 4 != 0:
                    volN = volN - volN % 4
                    if volN >= 0:
                        volN = 0
                    elif volN <= -64:
                        volN = -64
                    elif vol >= -11:
                        volN = vol


                volume.SetMasterVolumeLevel(vol, None)  # controling volume
        # if left hand is raised
        elif handtype[0] == "Right":

            #gesture control
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                x2, y2 = lmList[12][1], lmList[12][2]
                if distance([x1,y1],[x2,y2])<90:
                    PATH.append([x1,y1])
                if len(PATH)>6:
                    PATH.pop(0)
                if len(PATH)>5 and distance(PATH[0],PATH[-1])>240:
                    print(340, R_Sq(PATH))
                    if R_Sq(PATH)>0.68:
                        get_swipe_direction(PATH)

                        #function
                        pyautogui.hotkey('alt','esc')


            #close mouse
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if(length > 50):
                    break




    #11 frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #12 Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)