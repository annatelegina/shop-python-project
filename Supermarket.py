import random
import time

from Statistics import *
from CashDesk import *
from Utils import *

class Supermarket:
    def __init__(self, cash_desks=[3, 5], max_queue=3, \
            hours=[11, 8], discount=None, interval=30):

        self.__workday, self.__weekend = work_time[0]*60, work_time[1]*60
        self.__max_queue = max_queue
        self.__interval = interval

        self.adjustDiscount(discount)
        self.createDesks(cash_desks)

        self.__stat = Statistics()

    def workDay(self, number):
        currentTime = 9 * 60
        hours = self.__workday if number < 6 else self.__weekend
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
                    print("add")
            elif not start % interval:
                self.addCustomer()
                print("add")
            self.updateCashDesks()
            start += 1
            currentTime += 1
            time.sleep(0.2)

        print("Done ", number)


    def workWeek(self):
        for i in range(1, 8):
            self.workDay(i)
            time.sleep(1)

    def updateCashDesks(self):
        for i in self.__weekday:
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

    def createDesks(self, desks):
        day, weekend = desks
        self.__weekday = [CashDesk() for i in range(day)]
        self.__weekend = [CashDesk() for i in range(weekend)]
    
    def findMinQueue(self):
        min_q, ind = 10, 0
        for i in range(len(self.__weekday)):
            a = self.__weekday[i].quelen() 
            if a < min_q:
                min_q, ind = a, i

        return ind

    def addCustomer(self):
        customer = createCustomer()
        lengths = [self.__weekday[i].quelen() \
                for i in range(len(self.__weekday))]
        available = []
        for i in range(len(lengths)):
            if lengths[i] < self.__max_queue:
                available.append(i)

        if len(available) == 0:
            self.__stat.addLosed()
            print("LOSED")
        else:
            found = self.findMinQueue()
            self.__stat.addWaitTime(self.__weekday[found])
            self.__weekday[found].pushCustomer(customer)
            print(" Push to ", found)
            self.__stat.addCustomStat(customer)

