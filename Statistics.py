from Constant import *

class Statistics(object):
    def __init__(self, desks):

        self._desks = desks
        self._profit = 0
        self._lost_clients = 0
        self._done_clients = 0
        self._waiting = 0
        self.que_len = 0

    #-------------------------------------------------------
    #-----Public methods------------------------------------
    #-------------------------------------------------------
    
    def get_profit(self):
        return self._profit

    def add_lost(self):
        self._lost_clients += 1

    def update_custom_stat(self, client):
        self._done_clients += 1
        self._profit += client.get_sum()
        
    def current_clients(self):
        return self._los_clients, self._done_clients
        
    def update_waiting_time(self, cash_desk):
        total_time = 0
        for client in cash_desk.get_clients():
            total_time += client.get_time()

        self._waiting += total_time

    def update_queue(self, lengths):
        for clients in lengths:
            self.que_len += clients

    def prepare_stat(self, work_time):

        total = {}
        total["profit"] = self._profit \
                        - self._desks * SALARY

        total["avg_waiting"] = self._waiting / self._done_clients \
                        if self._done_clients > 0 else 0.

        total["avg_length"] = self.que_len \
                        / (work_time * self._desks)

        total["lost_clients"] = self._lost_clients
        total["acc_clients"] = self._done_clients

        return total
