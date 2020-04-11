from Supermarket import *
from Statistics import *
from Visualizer import *
from Utils import *
from Constant import *

from PyQt5.QtCore import Qt, QPoint, QBasicTimer

class World:
    def __init__(self):
        self.market = None
        self.cash_desk = [0, 0]
        self.work_hours = [8, 11]
        self.parameters = {
                "max_queue": 0
                }

    #----------------------------------------------------------------
    #-------Public methods-------------------------------------------
    #----------------------------------------------------------------

    def start_game(self):
        self.visualizer = Visualizer()
        self._adapt_functions()

    #---------------------------------------------------------------
    #------Private methods------------------------------------------
    #---------------------------------------------------------------

    def _adapt_functions(self):
        self.visualizer.buttons[0].clicked.connect(
            self._start_experiment
        )
        self.visualizer.titles[0].textChanged[str].connect(
            self._cash_desk_weekday
        )
        self.visualizer.titles[1].textChanged[str].connect(
            self._cash_desk_weekend
        )
        self.visualizer.titles[2].textChanged[str].connect(
            self._max_queue_len
        )
        self.visualizer.titles[3].textChanged[str].connect(
            self._work_hours_weekday
        )
        self.visualizer.titles[4].textChanged[str].connect(
            self._work_hours_weekend
        )
        self.visualizer.titles[5].textChanged[str].connect(
            self._set_interval
        )
        self.visualizer.sld.valueChanged.connect(
            self._adjust_discount
        )

    def _start_experiment(self):
        if not self.visualizer.paused:
            text = "Please click PAUSE or wait for the experiment end"
            message_box(self.visualizer, "Restarting error", text)
        else:
            if self.market:
                self.visualizer.kill()
                self.market = None
            text = self._check_config(self.parameters)
            if not text:
                self._start_working()
            else:
                message_box(self.visualizer, "Starting error", text)

    def _start_working(self):
        self.market = Supermarket(**self.parameters)
        self.visualizer.\
                start(
                    self.market, 
                    self.cash_desk, 
                    self.work_hours
                )

    #---------------------------------------------------------------------
    #------Functions to handle the input from the widget------------------
    #---------------------------------------------------------------------

    def _cash_desk_weekday(self, text):
        try:
            a = int(text)
            self.cash_desk[0] = a
        except ValueError:
            self.cash_desk[0] = 0    

    def _cash_desk_weekend(self, text):
        try:
            a = int(text)
            self.cash_desk[1] = a
        except ValueError:
            self.cash_desk[1] = 0

    def _work_hours_weekday(self, number):
        try:
            a = int(number)
            self.work_hours[0] = a
        except ValueError:
            self.work_hours[0] = 0

    def _work_hours_weekend(self, number):
        try:
            a = int(number)
            self.work_hours[1] = a
        except ValueError:
            self.work_hours[1] = 0

    def _set_interval(self, number):
        try:
            a = int(number)
            self.visualizer.paint_interval = a
        except ValueError:
            self.visualizer.paint_interval = 0

    def _max_queue_len(self, number):
        try:
            a = int(number)
            self.parameters["max_queue"] = a
        except ValueError:
            self.parameters["max_queue"] = 0

    def _adjust_discount(self, value):
        self.parameters["discount"] = float(value)/100

    def _check_config(self, config):
        text = ""
        if not self.work_hours[0] or not self.work_hours[1]:
            text += " Enter work hours! \n"
        if not self.cash_desk[0] or not self.cash_desk[1]:
            text += " Enter number of cash desks! \n"
        if not self.parameters["max_queue"]:
            text += " Enter the number of max queue length! \n"
        if not self.visualizer.paint_interval:
            text += " Enter the interval! \n"

        return text

