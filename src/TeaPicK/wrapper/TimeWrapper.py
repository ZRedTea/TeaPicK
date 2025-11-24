from datetime import datetime

class TimeWrapper:
    def __init__(self):
        self._time = datetime.now()
        self._create_time = datetime.now()

    def update(self, new_time):
        self._time = new_time

    @property
    def create_time(self):
        return self._create_time

    @property
    def time(self):
        return self._time

    def __str__(self):
        return str(self._time)