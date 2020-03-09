class Statistics:
    def __init__(self):
        self.__profit = 0
        self.__losed_clients = 0
        self.__done_clients = 0
        self.__average_occupation = 0

    def getProfit(self):
        return self.__profit

    def addLosed(self):
        self.__losed_clients += 1

    def addCustomStat(self, client):
        self.__done_clients += 1
        self.__profit += client.getSum()
