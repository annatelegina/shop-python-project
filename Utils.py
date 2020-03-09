import random

from Customer import *

def rush_hour(time):
    if time in range(17*60 + 30, 19*60):
        return True
    else:
        return False

def createCustomer():
    s = random.uniform(30, 1e+4)
    visitTime = random.uniform(1, 7)

    return Customer(s, visitTime)

