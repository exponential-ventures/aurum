import logging
import sys
import unittest

from aurum.logging_tracker import LoggingTracker


class LoggingTrackerTestCase(unittest.TestCase):

    def test_stdout(self):
        lt = LoggingTracker()
        print("hello world")
        lt.stdout.temp_file.seek(0)
        c = lt.stdout.temp_file.read()
        self.assertEqual(c, "hello world\n")

    def test_stderr(self):
        lt = LoggingTracker()
        print("hello world", file=sys.stderr)
        lt.stderr.temp_file.seek(0)
        c = lt.stderr.temp_file.read()
        self.assertEqual(c, "hello world\n")

    def test_logging_stdout(self):
        lt = LoggingTracker()
        logging.critical("hello world")
        lt.stdout.temp_file.seek(0)
        c = lt.stdout.temp_file.read()
        self.assertEqual(c, "hello world\n")


if __name__ == '__main__':
    unittest.main()
