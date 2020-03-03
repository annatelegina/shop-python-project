from collections import deque

class CashDesk(object):
    def __init__():
        self.__queue = deque()
        self.__margin = 0

    def getMargin(self):
        return self.__margin

    def pushCustomer(self, client):
        self.__queue.append(client)

    def popCustomer(self):
        self.__queue.popleft()

    def quelen(self):
        return len(self.__queue)
