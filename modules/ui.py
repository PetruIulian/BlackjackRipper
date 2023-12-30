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
from modules.strategyParse import basic_strategy

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

        self.resetBtn = QPushButton("Reset Count")
        self.resetBtn.clicked.connect(self.resetGame)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.cancelFeed)

        self.VBL.addWidget(self.resetBtn)
        self.VBL.addWidget(self.cancelBtn)


        # CARDS VBL LAYOUT
        self.bannerLabel = QLabel() 
        self.bannerLabel.setPixmap(QPixmap("files/banner.png"))
        self.bannerLabel.setAlignment(Qt.AlignCenter)
        self.bannerLabel.setScaledContents(True)

        self.myCards = QLabel("My Cards: ")
        self.myCards.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.myCards.setAlignment(Qt.AlignLeft)
        
        self.dealerCards = QLabel("Dealer Cards: ")
        self.dealerCards.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.dealerCards.setAlignment(Qt.AlignLeft)
        
        self.myValue = QLabel("My Value: ")
        self.myValue.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.myValue.setAlignment(Qt.AlignLeft)

        self.dealerValue = QLabel("Dealer Value: ")
        self.dealerValue.setStyleSheet("font: 20pt Comic Sans MS; color: white;")
        self.dealerValue.setAlignment(Qt.AlignLeft)

        self.actionLabel = QLabel(text="Waiting for action...")
        self.actionLabel.setAlignment(Qt.AlignCenter)
        self.actionLabel.setStyleSheet("font: 30pt Comic Sans MS; color: white; background: green;")

        self.cardsVBL.addWidget(self.bannerLabel)
        self.cardsVBL.addWidget(self.myCards)
        self.cardsVBL.addWidget(self.dealerCards)
        self.cardsVBL.addWidget(self.myValue)
        self.cardsVBL.addWidget(self.dealerValue)
        self.cardsVBL.addWidget(self.actionLabel)

        self.HBL.addLayout(self.cardsVBL, stretch=1)
        self.HBL.addLayout(self.VBL)

        self.worker = Worker(self.countLabel, self.myCards, self.dealerCards, self.actionLabel, self.myValue, self.dealerValue)
        self.worker.start()
        self.worker.ImageUpdate.connect(self.imageUpdateSlot)

        self.setLayout(self.HBL)

    def imageUpdateSlot(self, image):
        self.feedLabel.setPixmap(QPixmap.fromImage(image))

    def cancelFeed(self):
        self.worker.stop()

    def resetGame(self):
        global myCards
        global dealerCards
        myCards = []
        dealerCards = []
        self.countLabel.setText("Count: 0")
        self.myCards.setText("My Cards: ")
        self.dealerCards.setText("Dealer Cards: ")
        self.myValue.setText("My Value: ")
        self.dealerValue.setText("Dealer Value: ")

    

class Worker(QThread):

    def __init__(self, countLabel, myCardsLabel, dealerCardsLabel, action_label, myValue, dealerValue):
        super(Worker, self).__init__()
        self.count = 0
        self.countLabel = countLabel
        self.myCards = myCardsLabel
        self.dealerCards = dealerCardsLabel
        self.actionLabel = action_label
        self.myValue = myValue
        self.dealerValue = dealerValue

    ImageUpdate = pyqtSignal(QImage)

    def getTotals(self, mycards, dealearcards):
        player_total = 0
        for card in myCards:
            if card[1:] in ["2", "3", "4", "5", "6"]:
                player_total += int(card[1:])
            elif card[1:] in ["a", "b", "v", "h"]:
                player_total += 10
            else:
                player_total += 10

        dealer_value = 0
        for card in dealerCards:
            if card[1:] in ["2", "3", "4", "5", "6"]:
                dealer_value += int(card[1:])
            elif card[1:] in ["a", "b", "v", "h"]:
                dealer_value += 10
            else:
                dealer_value += 10

        return player_total, dealer_value

    def calculateCount(self, card):
        if card[1:] in ["2", "3", "4", "5", "6"]:
            self.count += 1
        elif card[1:] in ['10',"a", "b", "v", "h"]:
            self.count -= 1

    def run(self):
        global lastCard
        self.ThreadActive = True
        model = YOLO("best.pt")
        
        Capture = cv2.VideoCapture(0) # sau 0 pt camera de la laptop | "http://192.168.0.187:4747/video"
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

                    # check card y coord
                    if model.names[int(c)] != "j" and model.names[int(c)] != lastCard:
                        if b[1] > 250:
                            if model.names[int(c)] != 'pile-face-down' and model.names[int(c)] != 'pile-face-up':
                                if model.names[int(c)] not in myCards:
                                    myCards.append(model.names[int(c)])
                                    self.calculateCount(model.names[int(c)])
                                myCards.sort()
                            self.myCards.setText(f"My Cards: {' '.join(myCards)} ")
                        else:
                            if model.names[int(c)] != 'pile-face-down' and model.names[int(c)] != 'pile-face-up':
                                if model.names[int(c)] not in dealerCards:
                                    dealerCards.append(model.names[int(c)])
                                    self.calculateCount(model.names[int(c)])
                            dealerCards.sort()
                            self.dealerCards.setText(f"Dealer Cards: {' '.join(dealerCards)}")

                    lastCard = model.names[int(c)]
                self.countLabel.setText(f"Count: {self.count}")

                totals = self.getTotals(myCards, dealerCards)

                self.myValue.setText(f"My Value: {totals[0]}")
                self.dealerValue.setText(f"Dealer Value: {totals[1]}")

                action = basic_strategy(*self.getTotals(totals[0], totals[1]))
                if action == "hit":
                    self.actionLabel.setStyleSheet("font: 30pt Comic Sans MS; color: white; background: green;")
                    self.actionLabel.setText("Hit")
                elif action == "stand":
                    self.actionLabel.setStyleSheet("font: 30pt Comic Sans MS; color: white; background: red;")
                    self.actionLabel.setText("Stand")
                elif action == "double":
                    self.actionLabel.setStyleSheet("font: 30pt Comic Sans MS; color: white; background: blue;")
                    self.actionLabel.setText("Double")

                img = annotator.result()  
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.ImageUpdate.emit(QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888))

    def stop(self):
        self.ThreadActive = False
        self.quit()