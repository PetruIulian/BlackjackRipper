import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import ImageGrab
import numpy as np
from win32gui import FindWindow, GetWindowRect, GetForegroundWindow, GetWindowText

lastCard = ""
myCards = []
dealerCards = []

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        global myCards
        global dealerCards
        self.setFixedSize(1280, 720)
        self.setWindowTitle("BlackjackRipperr")
        self.setStyleSheet("background-color: gray;")

        self.HBL = QHBoxLayout()
        self.VBL = QVBoxLayout()
        self.cardsVBL = QVBoxLayout()

        # VBL LAYOUT
        self.feedLabel = QLabel()
        self.countLabel = QLabel(text="Count: 0")
        self.countLabel.setStyleSheet("font: 30pt Comic Sans MS; color: green;")
        self.VBL.addWidget(self.countLabel)
        self.VBL.addWidget(self.feedLabel)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelFeed)
        self.VBL.addWidget(self.cancelBtn)


        # CARDS VBL LAYOUT
        self.bannerLabel = QLabel() 
        self.bannerLabel.setPixmap(QPixmap("files/banner.png"))
        self.bannerLabel.setAlignment(Qt.AlignCenter)
        self.bannerLabel.setScaledContents(True)

        self.myCards = QLabel("My Cards: ")
        self.myCards.setStyleSheet("font: 30pt Comic Sans MS; color: white;")
        self.myCards.setAlignment(Qt.AlignLeft)
        
        self.dealerCards = QLabel("Dealer Cards: ")
        self.dealerCards.setStyleSheet("font: 30pt Comic Sans MS; color: white;")
        self.dealerCards.setAlignment(Qt.AlignLeft)
        

        self.actionLabel = QLabel(text="HIT")
        self.actionLabel.setAlignment(Qt.AlignCenter)
        self.actionLabel.setStyleSheet("font: 30pt Comic Sans MS; color: white; background: green;")

        self.cardsVBL.addWidget(self.bannerLabel)
        self.cardsVBL.addWidget(self.myCards)
        self.cardsVBL.addWidget(self.dealerCards)
        self.cardsVBL.addWidget(self.actionLabel)

        self.HBL.addLayout(self.cardsVBL, stretch=1)
        self.HBL.addLayout(self.VBL)

        self.worker = Worker(self.countLabel, self.myCards, self.dealerCards)
        self.worker.start()
        self.worker.ImageUpdate.connect(self.imageUpdateSlot)

        self.setLayout(self.HBL)

    def imageUpdateSlot(self, image):
        self.feedLabel.setPixmap(QPixmap.fromImage(image))

    def cancelFeed(self):
        self.worker.stop()

    def xInputChanged(self):
        global x_coord
        x_coord = self.xInput.value()
        x_coord += 50
    def yInputChanged(self):
        global y_coord
        y_coord = self.yInput.value()
        y_coord += 50
    def pos_xInputChanged(self):
        global pos_x
        pos_x = self.pos_xInput.value()
        pos_x += 50
    def pos_yInputChanged(self):
        global pos_y
        pos_y = self.pos_yInput.value()
        pos_y += 50
    

class Worker(QThread):

    def __init__(self, countLabel, myCardsLabel, dealerCardsLabel):
        super(Worker, self).__init__()
        self.count = 0
        self.countLabel = countLabel
        self.myCards = myCardsLabel
        self.dealerCards = dealerCardsLabel

    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        global lastCard
        self.ThreadActive = True
        model = YOLO("best.pt")
        
        Capture = cv2.VideoCapture("http://192.168.0.187:4747/video") # sau 0 pt camera de la laptop | "http://192.168.0.187:4747/video"
        Capture.set(3, 640)
        Capture.set(4, 480)
        while self.ThreadActive:

            _, img = Capture.read()
            results = model.predict(img)
            for r in results:
                
                annotator = Annotator(img)
            
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)])
                    
                    if model.names[int(c)][1:] != "j" and model.names[int(c)][1:] != lastCard[1:]:
                        if model.names[int(c)][1:] in ["2", "3", "4", "5", "6"]:
                            self.count += 1
                        elif model.names[int(c)][1:] in ['10',"a", "b", "v", "h"]:
                            self.count -= 1

                        # check card y coord
                        if model.names[int(c)][1:] != "j":
                            if b[1] < 200:
                                myCards.append(model.names[int(c)])
                                myCards.sort()
                                self.myCards.setText(f"My Cards: {' '.join(myCards)}")
                            else:
                                dealerCards.append(model.names[int(c)])
                                dealerCards.sort()
                                self.dealerCards.setText(f"Dealer Cards: {' '.join(dealerCards)}")

                    lastCard = model.names[int(c)]
                self.countLabel.setText(f"Count: {self.count}")
                    
                img = annotator.result()  
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.ImageUpdate.emit(QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888))

    def stop(self):
        self.ThreadActive = False
        self.quit()