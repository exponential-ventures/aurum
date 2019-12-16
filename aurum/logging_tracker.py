import logging
import sys
from tempfile import TemporaryFile

from aurum.common import SingletonMixin


class tee:
    """
    Inspired by: http://shallowsky.com/blog/programming/python-tee.html
    """

    def __init__(self, stream):
        self.temp_file = TemporaryFile(mode="w+")
        self.stream = stream

    def write(self, text):
        self.temp_file.write(text)
        self.stream.write(text)

    def flush(self):
        self.temp_file.flush()
        self.stream.flush()


class LoggingTracker(SingletonMixin):

    def __init__(self) -> None:
        super().__init__()

        self.stdout = tee(sys.stdout)
        self.stderr = tee(sys.stderr)
        logging.getLogger().addHandler(logging.StreamHandler(self.stdout.temp_file))

        sys.stdout = self.stdout
        sys.stderr = self.stderr
