import random
import Customer

def rush_hour(time):
    if time in range(17*60 + 30, 19*60):
        return True
    else:
        return False

def createCurtomers(number):
    customList = []
    for i in range(number):
        s = random.uniform(30, 1e+4)
        customList.append(Customer(s))

    return customList

