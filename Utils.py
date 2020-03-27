import random

from Customer import *
from Constant import *

def rush_hour(time):

    if time in range(RUSH_HOUR_START*60, RUSH_HOUR_END*60):
        return True
    else:
        return False

def createCustomer():
    s = random.normalvariate(AVG_SUM, STD_SUM)
    visitTime = int(random.uniform(1, 7))

    return Customer(s, visitTime)


def check_config(CONFIG):
    text = ""
    if not CONFIG["hours"][0] or not CONFIG["hours"][1]:
        text += " Enter work hours! \n"
    if not CONFIG["cash_desks"][0] or not CONFIG["cash_desks"][1]:
        text += " Enter number of cash desks! \n"
    if not CONFIG["max_queue"]:
        text += " Enter the number of max queue length! \n"
    if not CONFIG["interval"]:
        text += " Enter the interval! \n"
    return text

