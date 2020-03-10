from collections import deque

import Customer

class CashDesk():
    def __init__(self):
        self.__queue = deque()
        self.__margin = 0
        self.__startTime = 0

    def getMargin(self):
        return self.__margin

    def pushCustomer(self, client):
        self.__queue.append(client)

    def popCustomer(self):
        self.__queue.popleft()

    def quelen(self):
        return len(self.__queue)

    def clear(self):
        self.__queue.clear()

    def decreaseTime(self):
        if self.quelen() < 1:
            return
        print("LEN", self.quelen())
        self.__startTime += 1
        print(self.__queue[0].getTime(), " " , self.__startTime)
        if self.__queue[0].getTime() == self.__startTime:
            self.popCustomer()
            self.__startTime = 0

