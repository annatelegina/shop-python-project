import random

class Customer:
    def __init__(self, sum, time):
        self.__sum = sum
        self.__time = time

    def getSum(self):
        return self.__sum

    def getTime(self):
        return self.__time
