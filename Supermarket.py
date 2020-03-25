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
        self.__stat = Statistics()

    def workDay(self, number, visualizer):
        currentTime = START_TIME * 60
        hours = self.__weekday if number < 6 else self.__weekend
        hours += currentTime
        start = 0
        interval = 1
        while currentTime < hours:
            rush_ratio = 0.9 if rush_hour(currentTime) else 1.
            # update interval
            if (int(interval) and not start % interval) or not interval:
                start = 0
                interval = int(random.uniform(0, (7-number + 8)/2) * rush_ratio * self.__discount / 7)
            if not interval:
                c = int(random.uniform(0, 6))
                for i in range(c):
                    self.addCustomer()
            #        print("add")
            elif not start % interval:
                self.addCustomer()
             #   print("add")
            self.updateCashDesks()
            start += 1
            currentTime += 1
           # time.sleep(0.2)
            #if currentTime % self.__interval == 0:
                #visualizer.update(self.send_info(number))


        print("Done ", number)


    def workWeek(self, visualizer):
        for day in range(1, 8):
            self.workDay(day,visualizer)
            #time.sleep(1)

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


    def openDesks(self, desks):
        self.desks = [CashDesk() for i in range(desks)]

    def closeDesks(self):
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
            self.__stat.addLosed()
          #  print("LOSED")
        else:
            found = self.findMinQueue()
            #self.__stat.addWaitTime(self.__weekday[found])
            self.desks[found].pushCustomer(customer)
           # print(" Push to ", found)
            #self.__stat.addCustomStat(customer)


    def get_info(self):

        lengths = [self.desks[i].quelen() for i in range(len(self.desks))]

        print("GET_INFO", lengths)
        return lengths
