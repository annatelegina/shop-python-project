from Supermarket import *
from Statistics import *
from Visualizer import *
from Utils import *
from Constant import *


from PyQt5.QtCore import Qt, QPoint, QBasicTimer

CONFIG = {
        "max_queue": 0, 
        "discount": 0
}

BASELINE = CONFIG

class Runner:
    def __init__(self):


        self.cash_desk = [0, 0]
        self.work_hours_ = [11, 8]

        self.visualizer = Visualizer()
        self.adapt_functions()

    def adapt_functions(self):
        self.visualizer.button1.clicked.connect(self.start_experiment)
        self.visualizer.titleEdit.textChanged[str].connect(self.cashDesk_weekday)
        self.visualizer.titleEdit_2.textChanged[str].connect(self.cashDesk_weekend)
        self.visualizer.titleEdit_3.textChanged[str].connect(max_queue_len)
        self.visualizer.titleEdit_4.textChanged[str].connect(self.work_hours_weekday)
        self.visualizer.titleEdit_5.textChanged[str].connect(self.work_hours_weekend)
        self.visualizer.titleEdit_6.textChanged[str].connect(self.setInterval)
        self.visualizer.sld.valueChanged.connect(adjust_discount)

    def start_experiment(self):
        text = self.check_config(CONFIG)
        if not text:
            self.parameters = CONFIG
            self.start_working()
        else:
            mes = QMessageBox(self.visualizer)
            mes.setWindowTitle("Starting error")
            mes.setInformativeText(text)
            mes.exec_()

    def start_working(self):
        self.market = Supermarket(**self.parameters)
        self.visualizer.start(self.market, self.cash_desk, self.work_hours_)


    def cashDesk_weekday(self, text):
        try:
            a = int(text)
            self.cash_desk[0] = a
        except ValueError:
            self.cash_desk[0] = 0
    

    def cashDesk_weekend(self, text):
        try:
            a = int(text)
            self.cash_desk[1] = a
        except ValueError:
            self.cash_desk[1] = 0


    def work_hours_weekday(self, number):
        try:
            a = int(number)
            self.work_hours_[0] = a
        except ValueError:
            self.work_hours_[0] = 0


    def work_hours_weekend(number):
        try:
            a = int(number)
            self.work_hours_[1] = a
        except ValueError:
            self.work_hours_[1] = 0


    def setInterval(self, number):
        try:
            a = int(number)
            self.visualizer.interval = a
        except ValueError:
            self.visualizer.interval = 0


    def check_config(self, CONFIG):
        text = ""
        if not self.work_hours_[0] or not self.work_hours_[1]:
            text += " Enter work hours! \n"
        if not self.cash_desk[0] or not self.cash_desk[1]:
            text += " Enter number of cash desks! \n"
        if not CONFIG["max_queue"]:
            text += " Enter the number of max queue length! \n"
        if not self.visualizer.interval:
            text += " Enter the interval! \n"

        return text


def max_queue_len(number):
    try:
        a = int(number)
        CONFIG["max_queue"] = a
    except ValueError:
        CONFIG["max_queue"] = 0


def adjust_discount(value):
    CONFIG["discount"] = float(value)/100

