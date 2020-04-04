import sys
import time
import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QLineEdit, \
        QWidget, QSlider, QLabel, QPushButton,QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSlot, QBasicTimer, QTimer

from Supermarket import *
from Constant import *
from Utils import *


class Visualizer(QWidget):

    def __init__(self):
        super().__init__()

        self.time = QTimer()
        self.buttons = []
        self.titles = []
        self.paint_interval = 0
        self.days_of_week = DAYS_OF_WEEK

        self._set_functions()
        self._default_params()
        self._start_window()

    #--------------------------------------------------------------
    #------Public method-------------------------------------------
    #--------------------------------------------------------------

    def start(self, market, desks, hours):

        self.paused = False
        self.market = market
        self.cash_desks = desks
        self.work_hours = hours

        self._reset_timer()
        self.time.start(SPEED)
        self.time.timeout.connect(self.timerEvent)

        self.repaint()

    #-------------------------------------------------------------
    #------Private Methods----------------------------------------
    #-------------------------------------------------------------

    def _default_params(self):
        self.size = 8
        self.lengths = [MAX_CUSTOMERS for i in range(MAX_CASH_DESKS)]
        self.day = 0
        self.paused = True

        self.total = {
                "avg_waiting": 0, 
                "avg_length": 0,
                "profit": 0, 
                "lost_clients":0, 
                "acc_clients": 0
        }


    def _start_window(self):
        """
        Creates and vizualizes main window of the
             application with default parameters.
        """

        textLabel = QLabel(self)

        title = QLabel("Parameters of modeling", self)
        title.setFont(QtGui.QFont("Helvetica", 17.5, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.move(30,20)

        #create main buttons on the bottom of the window
        self._init_button("Start experiment", (150, 30), (50, 550))
        self._init_button("Pause/Continue", (150, 30), (50, 600), self.pause)
        self._init_button("Exit app", (150, 30), (50, 650), self.closeEvent)

        #create slider which allows to set up the discount
        self._init_discount_slider()
        
        #create and initialize the titles and lines for input parameters
        self._init_market_settings()

        #create labels for time and day of week 
        self.day_label = QLabel('Day: {:s}  '.format(self.days_of_week[0]), self)
        self.day_label.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        self.day_label.resize(1000, 50)
        self.time_label = QLabel('Time: 09:00', self)
        self.time_label.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        self.day_label.move(350, 500)
        self.time_label.move(350, 550)

        #create and initialize column for printing statistics
        #print the days of week
        self._init_stat_text()

        #create and initialize the main statistics
        self._init_day_scores()
        self._init_total_scores()

        #set the main parameters of window
        self.setGeometry(300,300,1200,900)
        self.setWindowTitle("Supermarket imitation")
        self.show()


    def _init_stat_text(self):
        """
        Initialize text for statistics and time
        """
        #for total statistics
        dayLabel = QLabel("Total statistics", self)
        dayLabel.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold))
        dayLabel.move(650, 450)

        #for 1-day statistics
        for i in range(WEEK):
            dayLabel = QLabel(self.days_of_week[i], self)
            dayLabel.setFont(QtGui.QFont("Helvetica", 18, QtGui.QFont.Bold))
            dayLabel.move(1020, 10+100*i)


    def _init_day_scores(self):
        """
        Initialize 1 day statistic scores for printing
        Creates PyQt Label with default value
        """

        self.lost_clients_scores = []
        self.done_clients_scores = [] 
        self.profit = [] 

        self.avg_waiting_time = []
        self.avg_length = []

        for i in range(WEEK):

            lost_clients = self._init_label(
                    'Lost clients: 0    ', 
                    QtGui.QFont("Helvetica", 14), 
                    (1020, 40 + 100*i)
            )
            self.lost_clients_scores.append(lost_clients)
            
            done_clients = self._init_label(
                    'Accepted cliens: 0    ',
                    QtGui.QFont("Helvetica", 14),
                    (1020, 60 + 100*i)
            )
            self.done_clients_scores.append(done_clients)

            profit = self._init_label(
                    'Money: {:5d} k   '.format(0),
                    QtGui.QFont("Helvetica", 14),
                    (1020, 80 + 100*i)
            )
            self.profit.append(profit)

            avg_waiting = self._init_label(
                     "AvgTime: \n  0  ",
                     QtGui.QFont("Helvetica", 14), 
                     (1200, 10 + 100*i)
            )
            self.avg_waiting_time.append(avg_waiting)

            avg_length = self._init_label(
                     " AvgLen: \n  0  ",
                     QtGui.QFont("Helvetica", 14), 
                     (1200, 60 + 100*i)
            )
            self.avg_length.append(avg_length)

    def _init_total_scores(self):
        """
        Initialize total week statistics scores 
                by creating PyQt Labels
        """

        self.total_lost = self._init_label(
              "Lost clients: 0      ",
              QtGui.QFont("Helvetica", 14),
              (660, 500)
        )
 
        self.total_acc = self._init_label(
              "Acc. clients: 0      ",
              QtGui.QFont("Helvetica", 14),
              (660, 530)
        )

        self.total_money = self._init_label(
              "Money: 0    k        ",
              QtGui.QFont("Helvetica", 14),
              (660, 560)
        )

        self.total_wait = self._init_label(
              "Avg waiting: 0        ",
              QtGui.QFont("Helvetica", 14),
              (660, 590)
        )

        self.total_length = self._init_label(
              "Avg length: 0        ",
              QtGui.QFont("Helvetica", 14),
              (660, 620)
        )


    def _init_label(self, text, setting, coord):
        """
        Creates label with input text and settings
        Located in coordinates coord
        """

        label = QLabel(text, self)
        label.setFont(setting)
        label.move(coord[0], coord[1])

        return label

    def _init_discount_slider(self):
        """
        Creates slider for discount value and title for it
        """

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setGeometry(130, 450, 150, 30)
        self.sld.setMinimum(0.0)
        self.sld.setMaximum(100.0)

        self.title = QLabel("Discount", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.move(30,455)

    def _init_button(self, text, size, coord, function=None):
        """
        Creates button with input text and size;
        Located in place with coordinates coord
        Function: if it is not None, execute it, when button was pushed
        """

        button = QPushButton(self)
        button.setText(text)
        button.setFixedSize(size[0], size[1])
        button.move(coord[0],coord[1])

        if function is not None:
            button.clicked.connect(function)

        self.buttons.append(button)

    def _init_title_edit(self, coord, text, mode=None):
        """
        Creates edit line with default text;
        Located in place with coordinates coord
        mode: can be either "text" or "placeholder";
        If mode is "text", text is printed in bold
        Otherwise: text is transparent gray
        """

        title = QLineEdit(self)
        title.move(coord[0], coord[1])
        if mode == "text":
            title.setText(text)
        else:
            title.setPlaceholderText(text)
        self.titles.append(title)

    def _init_market_settings(self):
        """
        Creates titles and edil lines for supermarket parameters
        """

        self.title_shop = QLabel("Shop settings", self)
        self.title_shop.setFont(
            QtGui.QFont("Helvetica", 15,QtGui.QFont.Bold)
        )

        self.title_shop.move(50, 260)
        
        self.title_shop_2 = QLabel("Time settings", self)
        self.title_shop_2.setFont(
            QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold)
        )

        self.title_shop_2.move(50, 50)
        
        #cashboxes on weekdays and weekends
        title = QLabel('Cashboxes \n on weekdays', self)
        title.move(30, 345)
        self._init_title_edit((130, 350), "From 1 to 8")

        title_2 = QLabel('Cashboxes \n on weekends', self)
        title_2.move(30, 395)
        self._init_title_edit((130, 400),\
                         "From 1 to 8", mode="placeholder")

        title_3 = QLabel('Max queue \n length', self)
        title_3.move(30, 295)
        self._init_title_edit((130, 300), \
                         "From 1 to 8", mode="placeholder")

        # work hours on weekdays and weekends
        title_4 = QLabel('Work hours \n on weekdays', self)
        title_4.move(30, 195)
        self._init_title_edit((130, 200), "8", mode="text")

        title_5 = QLabel('Work hours \n on weekends', self)
        title_5.move(30, 145)
        self._init_title_edit((130, 150), "11", mode="text")

        #interval of modeling
        title_6 = QLabel("Interval \n of modeling", self)
        title_6.move(30, 95)
        self._init_title_edit((130, 100), \
                    "From 10 to 60 min", mode="placeholder")


    def _set_functions(self):
        """
        Redefine handle functions for PyQt format
        """

        self.paintEvent = self._paint_event
        self.timerEvent = self._timer_event
        self.paintPaddle = self._paint_paddle
        self.closeEvent = self._close_event
        self.kill = self._kill
        self.pause = self._pause

    def _reset_timer(self):

        if self.day and self.day <= WEEK:
            self.market.close_day()
            self._update_total_score()

        if not self.day:
            self.day = 1
        else:
            self.day += 1

        if self.day > 7:
            self.time.stop()
            self.paused = True
            text = "Experiment is finished!"
            message_box(self, "Message", text)
        else:
            self.current_time = START_TIME * 60
            self.hours = self.work_hours[0]*60 if self.day < 6 \
                            else self.work_hours[1]*60

            self.size = self.cash_desks[0] if self.day < 6 \
                            else self.cash_desks[1]

            self.hours += self.current_time
            self.tick = 0
            self.client_interval = 1

            self.market.open_day(self.size)

    #-------------------------------------------------------------------------
    #-----Methods for statistics updating-------------------------------------
    #-------------------------------------------------------------------------

    def _update_score(self):
        index = self.day - 1
        info = self.market.current_stat.prepare_stat(self.hours)

        self.day_label.setText("Day: {:s}   ".format(str(self.days_of_week[index])))

        hour, minutes = set_time(self.current_time)
        hour = "0" + str(hour) if hour < 10 else str(hour)
        minutes = "00" if not minutes else str(minutes)
        self.time_label.setText('Time: {}:{}'.format(hour, minutes))

        self.avg_waiting_time[index].setText( \
                "AvgTime: \n  {:.3f}  ".format(info["avg_waiting"]))

        self.avg_length[index].setText( \
                "AvgLen: \n  {:.3f}  ".format(info["avg_length"]))

        self.done_clients_scores[index].setText( \
                'Accepted cliens: {:d} '.format(info["acc_clients"]))
        
        self.lost_clients_scores[index].setText( \
                'Lost clients: {:d} '.format(info["lost_clients"]))

        profit = int(info["profit"]/1000)
        self.profit[index].setText("Money: {:5d} k  ".format(profit))


    def _update_total_score(self, start=False):

        if not start:
            info = self.market.current_stat.prepare_stat(self.hours)
            self.total = make_new_dict(self.total, info, self.day)

        self.total_wait.setText( \
                "Avg waiting: {:.3f}    ".format(self.total["avg_waiting"]))

        self.total_length.setText( \
                "Avg length: {:.3f}   ".format(self.total["avg_length"]))

        profit = int(self.total["profit"]/1000)
        self.total_money.setText(\
                "Money: {:5d}  k     ".format(profit))

        self.total_acc.setText( \
                "Acc. clients: {:d}  ".format(self.total["acc_clients"]))

        self.total_lost.setText( \
                "Lost clients: {:d}  ".format(self.total["lost_clients"]))

    def _reset_stat_scores(self):
        
        self.day_label.setText('Day: {:10}  '.format(self.days_of_week[0]))
        self.time_label.setText('Time: 09:00 ')

        for i in range(WEEK):
            self.avg_waiting_time[i].setText("AvgTime: \n  0  ")
            self.avg_length[i].setText("AvgLen: \n  0  ")
            self.done_clients_scores[i].setText('Accepted cliens: 0 ')
            self.lost_clients_scores[i].setText('Lost clients: 0 ')
            self.profit[i].setText("Money: {:5d} k".format(0))

    #-----------------------------------------------------------------------------------
    #--------Widget events--------------------------------------------------------------
    #-----------------------------------------------------------------------------------

    def _close_event(self, event):
        self.close()

    def _kill(self):
        self.time.stop()
        self._reset_stat_scores()
        self._default_params()
        self._update_total_score(start=True)

    def _paint_event(self, e):
        painter = QPainter()
        painter.begin(self)
        self.paintPaddle(painter)
        painter.end()

    def _pause(self):
        if self.paused:
            self.paused = False
            self.time.start(SPEED)
        else:
            self.paused = True
            self.time.stop()

    def _paint_paddle(self, painter):
        for i in range(self.size):
            painter.setBrush(QColor(25, 80, 0, 160))
            painter.drawRect(350 + i*80, 20, 30, 30)

        for i in range(len(self.lengths)):
            for j in range(self.lengths[i]):
                painter.setPen(QPen(Qt.green,  8, Qt.DashLine))
                painter.drawEllipse(350 + i * 80, 60 + j*40, 20, 20)

    def _timer_event(self):

        if self.current_time > self.hours:
            self._reset_timer()

        if not self.client_interval or (int(self.client_interval) \
                            and not self.tick % self.client_interval):
            self.tick, self.client_interval = set_interval(
                self.current_time,
                self.day, 
                self.market.get_discount()
            )
        if not self.client_interval:
            c = int(random.uniform(0, MAX_CLIENTS_PER_MIN))
        elif not self.tick % self.client_interval:
            c = int(random.uniform(1, AVG_CLIENTS_PER_MIN))
        else:
            c = 0

        for i in range(c):
            self.market.add_customer()

        self.market.update_cash_desks()

        if self.current_time % self.paint_interval == 0:
            self.lengths.clear()
            self.lengths = self.market.get_info()
            self._update_score()

        self.market.update_cash_stat()
        self.current_time += 1
        self.tick += 1

        self.repaint()
