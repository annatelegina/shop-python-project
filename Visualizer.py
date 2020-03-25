import sys
import time
import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QLineEdit, QWidget, QSlider, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer, QTimer

from Supermarket import *
from Constant import *
from Utils import *

CONFIG = {
        "hours" : [8, 11],
        "cash_desks": [0, 0], 
        "max_queue": 0, 
        "discount": 0, 
        "interval": 0
}


class Visualizer(QWidget):

    def __init__(self):
        super().__init__()

        self.time = QTimer()
        self.size = 8
        self.lengths = [0 for i in range(8)]

        self.day = 0

        self.paused = False

        self.start_window()

    def start_window(self):

        textLabel = QLabel(self)

        title = QLabel("Parameters of modeling", self)
        title.setFont(QtGui.QFont("Helvetica", 17.5, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.move(30,20)

        self.button1 = QPushButton(self)
        self.button1.setText("Start experiment")
        self.button1.setFixedSize(200, 30)
        self.button1.move(150,650)

        self.button2 = QPushButton(self)
        self.button2.setText("Pause")
        self.button2.setFixedSize(200, 30)
        self.button2.move(450,650)
        self.button2.clicked.connect(self.pause)

        self.button3 = QPushButton(self)
        self.button3.setText("Exit app")
        self.button3.setFixedSize(200, 30)
        self.button3.move(750,650)
        
        self.init_discount_slider()
        self.init_window()

        self.setGeometry(300,300,1000,700)
        self.setWindowTitle("Supermarket imitation")
        self.show()

    def init_discount_slider(self):

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setGeometry(150, 600, 150, 30)
        self.sld.setMinimum(0.0)
        self.sld.setMaximum(100.0)

        self.title = QLabel("Discount", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(20,605)

    def init_window(self):

        self.title_shop = QLabel("Shop settings", self)
        self.title_shop.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        self.title_shop.move(50, 410)
        
        self.title_shop_2 = QLabel("Time settings", self)
        self.title_shop_2.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        self.title_shop_2.move(50, 200)
        
        title = QLabel('Cashboxes \n on weekdays', self)
        title.move(30, 495)
        self.titleEdit = QLineEdit(self)
        self.titleEdit.move(130, 500)
        self.titleEdit.setPlaceholderText("From 1 to 8")

        title_2 = QLabel('Cashboxes \n on weekends', self)
        title_2.move(30, 545)
        self.titleEdit_2 = QLineEdit(self)
        self.titleEdit_2.move(130, 550)
        self.titleEdit_2.setPlaceholderText("From 1 to 8")

        title_3 = QLabel('Max queue \n length', self)
        title_3.move(30, 445)
        self.titleEdit_3 = QLineEdit(self)
        self.titleEdit_3.move(130, 450)
        self.titleEdit_3.setPlaceholderText("From 1 to 8")

        # work hours
        title_4 = QLabel('Work hours \n on weekdays', self)
        title_4.move(30, 345)
        self.titleEdit_4 = QLineEdit(self)
        self.titleEdit_4.move(130, 350)
        self.titleEdit_4.setText("8")

        title_5 = QLabel('Work hours \n on weekends', self)
        title_5.move(30, 295)
        self.titleEdit_5 = QLineEdit(self)
        self.titleEdit_5.move(130, 300)
        self.titleEdit_5.setText("11")

        title_6 = QLabel("Interval \n of modeling", self)
        title_6.move(30, 245)
        self.titleEdit_6 = QLineEdit(self)
        self.titleEdit_6.move(130, 250)
        self.titleEdit_6.setPlaceholderText("From 10 to 60 min")

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.paintPaddle(painter)
        painter.end()

    def paintPaddle(self, painter):
        for i in range(self.size):
            painter.setBrush(QColor(25, 80, 0, 160))
            painter.drawRect(350 + i*80, 50, 30, 30)

        for i in range(len(self.lengths)):
            for j in range(self.lengths[i]):
                painter.setPen(QPen(Qt.green,  8, Qt.DashLine))
                painter.drawEllipse(350 + i * 80, 100 + j*70, 30, 30)


    def start(self, market, desks, hours):
        self.market = market
        self.cash_desks = desks
        self.work_hours = hours

        self.reset_timer()
        self.time.start(15)
        self.time.timeout.connect(self.timerEvent)

        self.repaint()

    def timerEvent(self):

        if self.currentTime == self.hours:
            self.reset_timer()

        rush_ratio = 0.9 if rush_hour(self.currentTime) else 1.

        if (int(self.interval_) and not self.start % self.interval_) or not self.interval_:
            self.start = 0
            self.interval_ = int(random.uniform(0, (7 + 8)/2) * rush_ratio * self.market.get_discount() / 7)
        if not self.interval_:
            c = int(random.uniform(0, 6))
            for i in range(c):
                self.market.addCustomer()
        elif not self.start % self.interval_:
            self.market.addCustomer()

        self.market.updateCashDesks()

        if self.currentTime % self.interval == 0:
            self.lengths.clear()
            self.lengths = self.market.get_info()
        print("HHH", self.size, self.lengths)
        self.currentTime += 1

        self.repaint()


    def reset_timer(self, day=1):

        if self.day:
            self.market.closeDesks()

        if not self.day:
            self.day = day
        else:
            self.day += 1

        if self.day  > 7:
            self.time.stop()
            return

        self.currentTime = START_TIME * 60

        self.hours = self.work_hours[0] if self.day < 6 else self.work_hours[1]
        self.size = self.cash_desks[0] if self.day < 6 else self.cash_desks[1]

        self.hours += self.currentTime

        self.start = 0
        self.interval_ = 1

        self.market.openDesks(self.size)

    def pause(self):
        if self.paused:
            self.paused = False
            self.time.start(15)
        else:
            self.paused = True
            self.time.stop()
