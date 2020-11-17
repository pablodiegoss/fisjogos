from .utils import SingletonMeta
from time import time
from enum import Enum


class TimedEvent(Enum):
    WIND_CHANGE = 20
    SHOOT = 1
    CAMERA = 0.1


class Cooldown(metaclass=SingletonMeta):
    time_table = {}

    def __init__(self):
        for event in TimedEvent:
            self.time_table[event] = time() + event.value

    def activate(self, timed_event):
        if self.time_table[timed_event] < time():
            self.time_table[timed_event] = time() + timed_event.value

    def check(self, timed_event):
        return self.time_table[timed_event] < time()