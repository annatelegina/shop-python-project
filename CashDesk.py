from collections import deque

class CashDesk(object):
    def __init__(self):
        self._clients = deque()
        self._margin = 0
        self._start_time = 0

    #------------------------------------
    #------Public methods----------------
    #------------------------------------

    def clients(self):
        return self._clients

    def queue_length(self):
        return len(self._clients)

    def get_margin(self):
        return self._margin

    def push_customer(self, new_client):
        self._clients.append(new_client)

    def clear(self):
        self._clients.clear()

    def decrease_timer(self):
        """
        Increase local timer in cash desk.
        It checks how much time if left 
        to handle the first client in queue.

        """

        if self.queue_length() < 1:
            return
        self._start_time += 1
        if self._clients[0].get_time() == self._start_time:
            self._pop_customer()
            self._start_time = 0

    #-----------------------------------
    #------Private methods--------------
    #-----------------------------------

    def _pop_customer(self):
        self._clients.popleft()


