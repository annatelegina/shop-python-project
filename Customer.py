class Customer(object):

    def __init__(self, sum_value, time):
        self._sum = sum_value
        self._time = time

    def get_sum(self):
        return self._sum

    def get_time(self):
        return self._time
