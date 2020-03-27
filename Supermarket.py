import random
import time

from Statistics import *
from CashDesk import *
from Utils import *
from Constant import *

class Supermarket:
    def __init__(self, max_queue=3, discount=None):

        self.__max_queue = max_queue
        self.adjustDiscount(discount)
        self.stats = []
        self.currentStat = None

    def updateCashDesks(self):
        for i in self.desks:
            i.decreaseTime()

    def adjustDiscount(self, discount):
        if not discount:
            self.__discount = 1.
        elif discount > 0.7:
            self.__discount = 0.7
        elif discount > 0.4:
            self.__discount = 0.8
        elif discount > 0.15:
            self.__discount = 0.9
        else:
            self.__discount = 1.

    def get_discount(self):
        return self.__discount

    def openDay(self, desks):
        if self.currentStat:
            self.stats.append(self.currentStat)
        self.currentStat = Statistics(desks)
        self.desks = [CashDesk() for i in range(desks)]

    def closeDay(self):
        self.desks.clear()

    def findMinQueue(self):
        min_q, ind = 10, 0
        for i in range(len(self.desks)):
            a = self.desks[i].quelen() 
            if a < min_q:
                min_q, ind = a, i

        return ind

    def addCustomer(self):
        customer = createCustomer()
        lengths = [self.desks[i].quelen() \
                for i in range(len(self.desks))]
        available = []
        for i in range(len(lengths)):
            if lengths[i] < self.__max_queue:
                available.append(i)

        if len(available) == 0:
            self.currentStat.addLosed()
        else:
            found = self.findMinQueue()
            self.currentStat.addWaitTime(self.desks[found])
            self.desks[found].pushCustomer(customer)
            self.currentStat.addCustomStat(customer)


    def update_cash_stat(self):
        lengths = [self.desks[i].quelen() for i in range(len(self.desks))]
        self.currentStat.updateQue(lengths)


    def get_info(self):
        lengths = [self.desks[i].quelen() for i in range(len(self.desks))]
        return lengths


