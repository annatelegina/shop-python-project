class Statistics:
    def __init__(self):
        self.__profit = 0
        self.__losed_clients = 0
        self.__done_clients = 0
        self.__waiting = 0

    def getProfit(self):
        return self.__profit

    def addLosed(self):
        self.__losed_clients += 1

    def addCustomStat(self, client):
        self.__done_clients += 1
        self.__profit += client.getSum()

    def addWaitTime(self, queue):
        time = 0
        for i in queue.queue():
            time += i.getTime()

        self.__waiting += time

    def printStat(self):
        pass

