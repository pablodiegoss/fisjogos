from .utils import SingletonMeta
from time import time
from enum import Enum


class TimedEvent(Enum):
    WIND_CHANGE = 20
    SHOT_TIMEOUT = 5


class Cooldown(metaclass=SingletonMeta):
    time_table = {}

    def __init__(self):
        for event in TimedEvent:
            self.time_table[event] = 0

    def activate(timed_event):
        if Cooldown().time_table[timed_event] < time():
            Cooldown().time_table[timed_event] = time() + timed_event.value

    def _activate(self, timed_event):
        if self.time_table[timed_event] < time():
            self.time_table[timed_event] = time() + timed_event.value

    def check(timed_event):
        return Cooldown()._check(timed_event)

    def _check(self, timed_event):
        return self.time_table[timed_event] < time()