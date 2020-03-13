import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QSlider, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot

CONFIG = {
        "hours" : [0, 0],
        "cash_desks": [0, 0], 
        "max_queue": 3, 
        "discount": None, 
        "interval":0
}

class Visualizer:
    def __init__(self):
        self.config = None

        self.start_window()

    def start_window(self):
        app = QApplication(sys.argv)
        widget = QWidget()
        textLabel = QLabel(widget)

        title = QLabel("Parameters of modeling", widget)
        title.setFont(QtGui.QFont("Helvetica", 17.5, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.move(30,20)

        button1 = QPushButton(widget)
        button1.setText("Start experiment")
        button1.setFixedSize(200, 30)
        button1.move(150,650)
#        button1.clicked.connect(button1_clicked)

        button2 = QPushButton(widget)
        button2.setText("Pause")
        button2.setFixedSize(200, 30)
        button2.move(450,650)
 #       button2.clicked.connect(button2_clicked)

        button3 = QPushButton(widget)
        button3.setText("Exit app")
        button3.setFixedSize(200, 30)
        button3.move(750,650)
  #      button3.clicked.connect(button2_clicked)
        
        self.init_discount_slider(widget)
        self.init_parameters(widget)
        widget.setGeometry(300,300,1000,700)
        widget.setWindowTitle("Supermarket imitation")
        widget.show()
        sys.exit(app.exec_())


    def init_discount_slider(self, widget):

        sld = QSlider(Qt.Horizontal, widget)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(150, 600, 150, 30)
        title = QLabel("Discount", widget)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.move(20,605)

        #TODO: Set the values of the slider

    def init_parameters(self, widget):

        title_shop = QLabel("Shop settings", widget)
        title_shop.move(50, 410)
        title_shop.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        
        title_shop = QLabel("Time settings", widget)
        title_shop.move(50, 200)
        title_shop.setFont(QtGui.QFont("Helvetica", 15, QtGui.QFont.Bold))
        
        title = QLabel('Cashboxes \n on weekdays', widget)
        title.move(30, 495)
        titleEdit = QLineEdit(widget)
        titleEdit.move(130, 500)
        titleEdit.setPlaceholderText("From 1 to 8")
        titleEdit.textChanged[str].connect(cashDesk_weekday)


        title_2 = QLabel('Cashboxes \n on weekends', widget)
        title_2.move(30, 545)
        titleEdit_2 = QLineEdit(widget)
        titleEdit_2.move(130, 550)
        titleEdit_2.setPlaceholderText("From 1 to 8")
        titleEdit_2.textChanged[str].connect(cashDesk_weekend)


        title_3 = QLabel('Max queue \n length', widget)
        title_3.move(30, 445)
        titleEdit_3 = QLineEdit(widget)
        titleEdit_3.move(130, 450)
        titleEdit_3.setPlaceholderText("From 1 to 8")
        titleEdit_3.textChanged[str].connect(max_queue_len)

        # work hours
        title_4 = QLabel('Work hours \n on weekdays', widget)
        title_4.move(30, 345)
        titleEdit_4 = QLineEdit(widget)
        titleEdit_4.move(130, 350)
        titleEdit_4.setText("8")
        titleEdit_4.textChanged[str].connect(work_hours_weekday)

        title_5 = QLabel('Work hours \n on weekends', widget)
        title_5.move(30, 295)
        titleEdit_5 = QLineEdit(widget)
        titleEdit_5.move(130, 300)
        titleEdit_5.setText("11")
        titleEdit_5.textChanged[str].connect(work_hours_weekend)

        title_6 = QLabel("Interval \n of modeling", widget)
        title_6.move(30, 245)
        titleEdit_6 = QLineEdit(widget)
        titleEdit_6.move(130, 250)
        titleEdit_6.setPlaceholderText("From 10 to 60 min")
        titleEdit_6.textChanged[str].connect(setInterval)


def cashDesk_weekday(text):
    try:
        a = int(text)
        CONFIG["cash_desks"][0] = a
    except ValueError:
        CONFIG["cash_desks"][0] = 0
    

def cashDesk_weekend(text):
    try:
        a = int(text)
        CONFIG["cash_desks"][1] = a
    except ValueError:
        CONFIG["cash_desks"][1] = 0


def max_queue_len(number):
    try:
        a = int(number)
        CONFIG["max_queue"] = a
    except ValueError:
        CONFIG["max_queue"] = 0


def work_hours_weekday(number):
    try:
        a = int(number)
        CONFIG["hours"][0] = a
    except ValueError:
        CONFIG["hours"][0] = 0


def work_hours_weekend(number):
    try:
        a = int(number)
        CONFIG["hours"][1] = a
    except ValueError:
        CONFIG["hours"][1] = 0

def setInterval(number):
    try:
        a = int(number)
        CONFIG["interval"] = a
    except ValueError:
        CONFIG["interval"] = 0

