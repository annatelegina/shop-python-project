import random

import Cashdesk
import utils

class Supermarket(Object):
    def __init__(work_time=[11, 8], cash_desks, max_queue, \
            discount=None, interval=30):
        self.__wokrday, self.__weekend = work_time[0]*60, work_time[1]*60
        self.__max_queue = max_queue
        self.__interval = interval

        self.adjustDiscount(discount)
        self.createDesks(cash_desks)

    def workDay(number):
        currentTime = 9 * 60
        hours = self.__workday if number < 6 else self.__weekend
        while currentTime < hours:
            rush_ratio = 0.9 if rush_hour(currentTime) else 1.
            customers = random.uniform(1, 7) * (-number + 8) * \
                    rush_ratio * self.__discount / 7
            c_number = self.__interval // customers
            customers = createCustomers(c_number)



    def workWeek():
        pass

    def adjustDiscount(self, discount):
        if discount > 0.7:
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
        
