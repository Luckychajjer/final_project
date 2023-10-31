import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
# print(listShirts)
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
scale_percent = 50 # percent of original size
width = int(imgButtonRight.shape[1] * scale_percent / 100)
height = int(imgButtonRight.shape[0] * scale_percent / 100)
dim = (width, height)
imgButtonRight = cv2.resize(imgButtonRight,dim)
imgButtonLeft = cv2.resize(imgButtonLeft,dim)
counterRight = 0
counterLeft = 0
selectionSpeed = 20


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    frame1 = detector.findPose(img,draw=False)
    lmList, bboxInfo = detector.findPosition(frame1, bboxWithHands=False, draw=False)
    if lmList:
        # center = bboxInfo["center"]
        lm11 = lmList[11][:2]
        lm12 = lmList[12][:2]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (500,220))
        img = cvzone.overlayPNG(img, imgButtonLeft, (50,220))

        if lmList[16][0] < 180:
            counterRight += 1
            cv2.ellipse(img, (82,252), (32,32), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 10)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
                else:
                    imageNumber = 0

        elif lmList[15][0] >420 :
            counterLeft += 1
            cv2.ellipse(img, (532,252), (32,32), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 10)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
                else:
                    imageNumber = len(listShirts) - 1

        else:
            counterRight = 0
            counterLeft = 0
    
    cv2.namedWindow('Pose Detection', cv2.WND_PROP_FULLSCREEN) #for full screen
    cv2.setWindowProperty('Pose Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) # for fullscreen
    cv2.resizeWindow('Pose Detection', 1280, 720) 
    cv2.imshow("Pose Detection",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()