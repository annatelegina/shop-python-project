from Constant import *

class Statistics:
    def __init__(self, desks):

        self.__desks = desks

        self.__profit = 0
        self.__losed_clients = 0
        self.__done_clients = 0
        self.__waiting = 0

        self.que_len = 0

        self.total = {}

    def getProfit(self):
        return self.__profit

    def addLosed(self):
        self.__losed_clients += 1

    def addCustomStat(self, client):
        self.__done_clients += 1
        self.__profit += client.getSum()
        
    def currentClients(self):
        return self.__losed_clients, self.__done_clients
        
    def addWaitTime(self, queue):
        time = 0
        for i in queue.queue():
            time += i.getTime()

        self.__waiting += time

    def updateQue(self, list):

        for i in list:
            self.que_len += i

    def prepareStat(self, work_time):
        self.total["profit"] = self.__profit - self.__desks * SALARY
        self.total["avg_waiting"] = self.__waiting / self.__done_clients if self.__done_clients > 0 else 0.
        self.total["avg_length"] = self.que_len / (work_time * self.__desks)

        return self.total
