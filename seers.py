from pyclick.humanclicker import HumanClicker
from pyclick.humancurve import HumanCurve
import pyautogui
import itertools
import random
import time
import math
import sys

class Seers():

    def __init__(self):
        # stage_num: ["needle.png","needle_fail.png",predicted_x,predicted_y,x_buffer,y_buffer]
        # needle.png - Image to search for on your screen (the next obstacle to click)
        # needle_fail.png - Detect a failed obstacle and reset to stage 0
        # predicted_x - x coordinate we expect the next obstacle to be at
        # predicted_y - y coordinate we expect the next obstacle to be at
        # x_buffer - Clickable x pixels +/- the center of the coordinates of the obstacle
        # y_buffer - Clickable y pixels +/- the center of the coordinates of the obstacle

        self.stages = {
            0: ["0_stage0.PNG", None, 1942, 113, 2, 2],
            1: ["1_stage1.PNG", None, 1956, 104, 3, 3],
            2: ["2_stage2.PNG", None, 1271, 644, 10, 50],
            3: ["3_stage3.PNG", "f_stage2.PNG", 907, 609, 10, 10],
            4: ["4_stage4.PNG", "f_stage3.PNG", 1122, 939, 75, 10],
            5: ["5_stage5.PNG", None, 1343, 889, 50, 10],
            6: ["6_stage6.PNG", None, 853, 839, 10, 50],
        }
        self.stage = 1
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.status = ""

    def print_status(self, msg: str, overwrite=False):
        last_msg_length = len(self.status)
        if overwrite:
            print(' ' * last_msg_length, end='\r')
            print(msg, end='\r')
            sys.stdout.flush()
        else:
            print(msg,' ' * last_msg_length)
        self.status = msg

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
        duration = random.randint(50, 80)
        pyautogui.PAUSE = (duration/100) / len(curve.points)

        self.print_status("Moving to {},{} ({}ms)".format(x,y,duration))
        for point in curve.points:
            pyautogui.moveTo(point)

    def click(self):
        hc = HumanClicker()
        time.sleep(random.randint(30, 120) / 1000)
        if random.randint(1, 4) == 2:
            for x in range(0, random.randint(2, 3)):
                delay = random.randint(45, 115) / 1000
                self.print_status("Multi Click {} ({}ms)".format(x,delay*1000))
                hc.click()
                time.sleep(delay)
        else:
            self.print_status("Single Click")
            hc.click()


    def performStage(self, pos, click=True, buffer=True):
        _,_,px,py,xrand,yrand = self.stages.get(self.stage)
        x,y = pos

        if buffer:
            x = x + random.randint(-xrand, xrand)
            y = y + random.randint(-yrand, yrand)

        self.moveToPosition(x,y)

        if click:
            self.click()
            self.stage += 1
            if self.stage == len(self.stages):
                self.stage = 0

        if random.randint(1, 2) == 2:
            if random.randint(1, 4) == 2:
                xr = random.randint(0, 2560)
                yr = random.randint(0, 1440)
                self.moveToPosition(xr,yr)
            else:
                px = px + random.randint(100, 200)
                py = py + random.randint(100, 200)
                self.moveToPosition(px,py)


    def attemptStage(self):
        self.print_status("{} Attempting stage {}".format(next(self.spinner),self.stage),True)
        sys.stdout.flush()

        image,image_fail,_,_,_,_ = self.stages.get(self.stage)
        pos = pyautogui.locateCenterOnScreen(image) #
        if pos != None:
            self.print_status("--- Performing stage {}".format(self.stage))
            self.performStage(pos)
        elif image_fail != None:
            self.print_status("{} Attempting stage {} (Checking for failure)".format(next(self.spinner),self.stage),True)
            sys.stdout.flush()

            posf = pyautogui.locateCenterOnScreen(image_fail)
            if posf != None:
                self.print_status("--- Failed stage {}, recovering".format(self.stage-1))
                self.performStage(posf, buffer=False)
                self.stage = 1

seers = Seers()
while True:
    seers.attemptStage()
