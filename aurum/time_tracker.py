import logging
from datetime import datetime, timedelta

from .singleton import SingletonDecorator


@SingletonDecorator
class TimeTracker:
    def __init__(self):
        self.initial_time = datetime.now()

    def log_time(self) -> timedelta:
        delta = datetime.now() - self.initial_time
        logging.info(f"The experiment took {str(delta)} to run")

        return delta


time_tracker = TimeTracker()
