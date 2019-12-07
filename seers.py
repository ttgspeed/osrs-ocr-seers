from pyclick.humanclicker import HumanClicker
from pyclick.humancurve import HumanCurve
import pyautogui
import random
import time
import math

class Seers():

    def __init__(self):
        self.stages = {
            -1: ["0_stage0.PNG", None, 1942, 113, 2, 2],
            0: ["1_stage1.PNG", None, 1956, 104, 3, 3],
            1: ["2_stage2.PNG", None, 1271, 644, 10, 50],
            2: ["3_stage3.PNG", None, 907, 609, 10, 10],
            3: ["4_stage4.PNG", "f_stage3.PNG", 1122, 939, 75, 10],
            4: ["5_stage5.PNG", None, 1343, 889, 50, 10],
            5: ["6_stage6.PNG", None, 853, 839, 10, 50],
        }
        self.stage = 0

    def generateRandomCurve(self,tx,ty):
        fx,fy = pyautogui.position()
        distance = math.sqrt( ((fx-tx)**2)+((fy-ty)**2) )

        curves = 3
        if distance < 1000:
            curves = 2
        if distance < 500:
            curves = 1

        return HumanCurve((int(fx),int(fy)), (int(tx),int(ty)), knotsCount=random.randint(1, curves))

    def moveToPosition(self,x,y):
        curve = self.generateRandomCurve(x,y)
        pyautogui.PAUSE = (random.randint(50, 80)/100) / len(curve.points)
        for point in curve.points:
            pyautogui.moveTo(point)

    def click(self):
        hc = HumanClicker()
        time.sleep(random.randint(30, 120) / 1000)
        if random.randint(1, 3) == 2:
            for x in range(0, random.randint(2, 3)):
                print("click")
                hc.click()
                time.sleep(random.randint(45, 115) / 1000)
        else:
            hc.click()


    def performStage(self, pos, click=True):
        _,_,px,py,xrand,yrand = self.stages.get(self.stage)
        x,y = pos
        x = x + random.randint(-xrand, xrand)
        y = y + random.randint(-yrand, yrand)

        self.moveToPosition(x,y)

        if click:
            self.click()
            self.stage = self.stage + 1
            if self.stage == 6:
                self.stage = -1

        if random.randint(1, 2) == 2:
            if random.randint(1, 4) == 2:
                xr = random.randint(0, 2560)
                yr = random.randint(0, 1440)
                self.moveToPosition(xr,yr)
            else:
                print("predicting",px,py)
                px = px + random.randint(100, 200)
                py = py + random.randint(100, 200)
                self.moveToPosition(px,py)


    def attemptStage(self):
        print("Attempting stage", self.stage)
        image,image_fail,_,_,_,_ = self.stages.get(self.stage)
        pos = pyautogui.locateCenterOnScreen(image) #
        if pos != None:
            print(pos)
            self.performStage(pos)
        elif image_fail != None:
            print("Checking for failure on stage", self.stage)
            posf = pyautogui.locateCenterOnScreen(image_fail)
            if posf != None:
                self.performStage(posf)
                self.stage = 0

seers = Seers()
while True:
    seers.attemptStage()
