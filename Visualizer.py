import sys
import time
import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QLineEdit, QWidget, QSlider, QLabel, QPushButton,QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
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

        self.def_params()
        self.start_window()

    def def_params(self):
        self.size = 8
        self.lengths = [8 for i in range(8)]

        self.desks = []
        self.day = 0
        self.paused = True


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
        self.button3.clicked.connect(self.closeEvent)
        self.init_discount_slider()
        self.init_window()

        self.dayLabel = QLabel('Day: 1', self)
        self.dayLabel.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        self.timeLabel = QLabel('Time: 09:00', self)
        self.timeLabel.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        self.dayLabel.move(30, 500)
        self.timeLabel.move(30, 550)

        self.init_stat_text()
        self.init_stat_scores()

        self.setGeometry(300,300,1200,900)
        self.setWindowTitle("Supermarket imitation")
        self.show()

    def init_stat_text(self):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(7):
            dayLabel = QLabel(days_of_week[i], self)
            dayLabel.setFont(QtGui.QFont("Helvetica", 18, QtGui.QFont.Bold))
            dayLabel.move(1020, 10+100*i)


    def init_stat_scores(self):
        self.lost_clients_scores = [None for i in range(7)]
        self.done_clients_scores = [None for i in range(7)]
        self.profit = [None for i in range(7)]

        self.avg_waiting_time = [None for i in range(7)]
        self.avg_length = [0 for i in range(7)]

        for i in range(7):
            self.lost_clients_scores[i] = QLabel('Lost clients: 0    ', self)
            self.lost_clients_scores[i].setFont(QtGui.QFont("Helvetica", 14))
            self.lost_clients_scores[i].move(1020, 40+100*i)

            self.done_clients_scores[i] = QLabel('Accepted cliens: 0    ', self)
            self.done_clients_scores[i].setFont(QtGui.QFont("Helvetica", 14))
            self.done_clients_scores[i].move(1020, 60+100*i)

            self.profit[i] = QLabel('Money: {:5d} k   '.format(0), self)
            self.profit[i].setFont(QtGui.QFont("Helvetica", 14))
            self.profit[i].move(1020, 80 + 100*i)

            self.avg_waiting_time[i] = QLabel("AvgTime: \n  0  ", self)
            self.avg_waiting_time[i].setFont(QtGui.QFont("Helvetica", 14))
            self.avg_waiting_time[i].move(1200, 10 + 100*i)

            self.avg_length[i] = QLabel(" AvgLen: \n  0  ", self)
            self.avg_length[i].setFont(QtGui.QFont("Helvetica", 14))
            self.avg_length[i].move(1200, 60 + 100*i)

    def init_discount_slider(self):

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setGeometry(130, 450, 150, 30)
        self.sld.setMinimum(0.0)
        self.sld.setMaximum(100.0)

        self.title = QLabel("Discount", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(30,455)

    def init_window(self):

        self.title_shop = QLabel("Shop settings", self)
        self.title_shop.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        self.title_shop.move(50, 260)
        
        self.title_shop_2 = QLabel("Time settings", self)
        self.title_shop_2.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        self.title_shop_2.move(50, 50)
        
        title = QLabel('Cashboxes \n on weekdays', self)
        title.move(30, 345)
        self.titleEdit = QLineEdit(self)
        self.titleEdit.move(130, 350)
        self.titleEdit.setPlaceholderText("From 1 to 8")

        title_2 = QLabel('Cashboxes \n on weekends', self)
        title_2.move(30, 395)
        self.titleEdit_2 = QLineEdit(self)
        self.titleEdit_2.move(130, 400)
        self.titleEdit_2.setPlaceholderText("From 1 to 8")

        title_3 = QLabel('Max queue \n length', self)
        title_3.move(30, 295)
        self.titleEdit_3 = QLineEdit(self)
        self.titleEdit_3.move(130, 300)
        self.titleEdit_3.setPlaceholderText("From 1 to 8")

        # work hours
        title_4 = QLabel('Work hours \n on weekdays', self)
        title_4.move(30, 195)
        self.titleEdit_4 = QLineEdit(self)
        self.titleEdit_4.move(130, 200)
        self.titleEdit_4.setText("8")

        title_5 = QLabel('Work hours \n on weekends', self)
        title_5.move(30, 145)
        self.titleEdit_5 = QLineEdit(self)
        self.titleEdit_5.move(130, 150)
        self.titleEdit_5.setText("11")

        title_6 = QLabel("Interval \n of modeling", self)
        title_6.move(30, 95)
        self.titleEdit_6 = QLineEdit(self)
        self.titleEdit_6.move(130, 100)
        self.titleEdit_6.setPlaceholderText("From 10 to 60 min")

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.paintPaddle(painter)
        painter.end()

    def paintPaddle(self, painter):
        for i in range(self.size):
            painter.setBrush(QColor(25, 80, 0, 160))
            painter.drawRect(350 + i*80, 20, 30, 30)

        for i in range(len(self.lengths)):
            for j in range(self.lengths[i]):
                painter.setPen(QPen(Qt.green,  8, Qt.DashLine))
                painter.drawEllipse(350 + i * 80, 60 + j*40, 20, 20)


    def start(self, market, desks, hours):

        self.paused = False
        self.market = market
        self.cash_desks = desks
        self.work_hours = hours

        self.reset_timer()
        self.time.start(SPEED)
        self.time.timeout.connect(self.timerEvent)

        self.repaint()

    def timerEvent(self):

        if self.currentTime > self.hours:
            self.reset_timer()

        rush_ratio = 0.6 if rush_hour(self.currentTime) else 1.

        if (int(self.interval_) and not self.start_ % self.interval_) or not self.interval_:
            self.start_ = 0
            self.interval_ = int(random.uniform(0, ((11 - self.day)**2/(15-self.day)) * rush_ratio * self.market.get_discount()))

        if not self.interval_:
            c = int(random.uniform(0, 6))
            for i in range(c):
                self.market.addCustomer()
        elif not self.start_ % self.interval_:
            c = int(random.uniform(1, 4))
            for i in range(c):
                self.market.addCustomer()

        self.market.updateCashDesks()

        if self.currentTime % self.interval == 0:
            self.lengths.clear()
            self.lengths = self.market.get_info()
            self.updateScore()

        self.market.update_cash_stat()
        self.currentTime += 1
        self.start_ += 1

        self.repaint()


    def reset_timer(self, day=1):

        if self.day and self.day <= 7:
            self.market.closeDay()

        if not self.day:
            self.day = day
        else:
            self.day += 1

        if self.day > 7:
            self.time.stop()
            mes = QMessageBox(self)
            mes.setWindowTitle("Message")
            mes.setInformativeText("Experiment is finished!")
            mes.exec_()
        else:
            self.currentTime = START_TIME * 60
            self.hours = self.work_hours[0]*60 if self.day < 6 else self.work_hours[1]*60
            self.size = self.cash_desks[0] if self.day < 6 else self.cash_desks[1]
            self.hours += self.currentTime
            self.start_ = 0
            self.interval_ = 1

            self.market.openDay(self.size)

    def pause(self):
        if self.paused:
            self.paused = False
            self.time.start(SPEED)
        else:
            self.paused = True
            self.time.stop()

    def updateScore(self):
        self.dayLabel.setText('Day: {}'.format(str(self.day)))
        hour = int(self.currentTime / 60)
        minutes = self.currentTime - hour * 60
        self.timeLabel.setText('Time: {:2d}:{:2d}'.format(hour, minutes))

        
        info = self.market.currentStat.prepareStat(self.hours)
        self.avg_waiting_time[self.day-1].setText("AvgTime: \n  {:.3f}  ".format(info["avg_waiting"]))
        self.avg_length[self.day-1].setText("AvgLen: \n  {:.3f}  ".format(info["avg_length"]))

        losed, done = self.market.currentStat.currentClients()
        self.done_clients_scores[self.day-1].setText('Accepted cliens: {:d} '.format(done))
        self.lost_clients_scores[self.day-1].setText('Lost clients: {:d} '.format(losed))
        profit = int(self.market.currentStat.getProfit()/1000)
        self.profit[self.day-1].setText("Money: {:5d} k  ".format(profit))

    def reset_stat_scores(self):
        
        self.dayLabel.setText('Day: 1 ')
        self.timeLabel.setText('Time: 09:00 ')

        for i in range(7):
            self.avg_waiting_time[i].setText("AvgTime: \n  0  ")
            self.avg_length[i].setText("AvgLen: \n  0  ")
            self.done_clients_scores[i].setText('Accepted cliens: 0 ')
            self.lost_clients_scores[i].setText('Lost clients: 0 ')
            self.profit[i].setText("Money: {:5d} k".format(0))

    def closeEvent(self, event):
        self.close()

    def kill(self):
        self.time.stop()
        self.reset_stat_scores()
        self.def_params()


