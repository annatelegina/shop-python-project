import random
import time

from Statistics import *
from CashDesk import *
from Utils import *
from Constant import *

class Supermarket(object):
    def __init__(self, max_queue=3, discount=None):

        self._max_queue = max_queue
        self._adjust_discount(discount)
        self.current_stat = None

    #-----------------------------------------------------
    #------Public methods---------------------------------
    #-----------------------------------------------------

    def get_discount(self):
        return self._discount

    def open_day(self, desks):
        self.current_stat = Statistics(desks)
        self.desks = [CashDesk() for i in range(desks)]

    def close_day(self):
        self.desks.clear()

    def add_customer(self):
        customer = create_customer()
        lengths = self.get_info()

        available = []
        for i in range(len(lengths)):
            if lengths[i] < self._max_queue:
                available.append(i)

        if len(available) == 0:
            self.current_stat.add_lost()
        else:
            found = self._find_cash_desk()

            self.current_stat.update_waiting_time(
                    self.desks[found]
            )
            self.current_stat.update_custom_stat(
                    customer
            )

            self.desks[found].push_customer(customer)

    def get_info(self):
        lengths = [self.desks[i].queue_length() 
                        for i in range(len(self.desks))]
        return lengths

    def update_cash_stat(self):
        lengths = self.get_info()
        self.current_stat.update_queue(lengths)

    def update_cash_desks(self):
        for desk in self.desks:
            desk.decrease_timer()

    #--------------------------------------------------------
    #------Private methods-----------------------------------
    #--------------------------------------------------------

    def _adjust_discount(self, discount):
        if not discount:
            self._discount = 1.
        elif discount > 0.7:
            self._discount = 0.7
        elif discount > 0.4:
            self._discount = 0.8
        elif discount > 0.15:
            self._discount = 0.9
        else:
            self._discount = 1.

    def _find_cash_desk(self):
        current_min, pos = 10, 0

        for i in range(len(self.desks)):
            length = self.desks[i].queue_length()
            if length < current_min:
                current_min, pos = length, i

        return pos

