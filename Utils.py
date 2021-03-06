import random

from PyQt5.QtWidgets import QMessageBox
from Customer import *
from Constant import *

def make_new_dict(old_dict, new_dict, param):
    """
    Make new dictionary for week statistics accumulation.
    Input: old_dict: previous information;
           new_dict: current day information;
           param: day of week.
    Output: new dictionary
    """

    if param == 1:
        return new_dict

    result = {}
    for key in old_dict.keys():
        if "avg_" in key:
            result[key] = (old_dict[key] * (param - 1) + new_dict[key]) / param
        else:
            result[key] = old_dict[key] + new_dict[key]

    return result


def set_time(mins):
    """
    Parse time from minutes to hours and minutes.
    """

    hour = int(mins / 60)
    minutes = mins - hour * 60

    return hour, minutes

#---------------------------------------------------------------
#-------Customer scheduling utils-------------------------------
#---------------------------------------------------------------

def is_rush_hour(time):
    if time in range(RUSH_HOUR_START*60, RUSH_HOUR_END*60):
        return True
    else:
        return False

def create_customer():
    """
    Create custmomer.
    Creates the puchase amount and time for handling.
    Output: Customer object.
    """

    s = random.normalvariate(AVG_SUM, STD_SUM)
    visitTime = int(random.uniform(1, 7))

    return Customer(s, visitTime)

def set_interval(current_time, day, discount):
    """
    Set the intensity of coming clients.
    Input: current_time of the day; day of week; amount of discount.
    Output: new interval and new start point.
    """

    rush_ratio = 0.6 if is_rush_hour(current_time) else 1.
    new_start = 0
    new_interval = int(random.uniform(0, ((11 - day)**2/(15-day)) * rush_ratio * discount))

    return new_start, new_interval

#----------------------------------------------------------
#-----PyQt Widget utils------------------------------------
#-----------------------------------------------------------

def message_box(visualizer, title, text):
    
    mes = QMessageBox(visualizer)
    mes.setWindowTitle(title)
    mes.setInformativeText(text)
    mes.exec_()
