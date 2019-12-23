import time


class Benchmark:
    def __init__(self, name: str):
        self.labels = []
        self.name = name

    def start(self):
        self.labels.append(('Start', time.time()))

    def end(self):
        self.labels.append(('End', time.time()))

    def add_label(self, name: str):
         self.labels.append((name, time.time()))

    def print(self):
        print('')
        print(self.name)
        print('')
        for label_index in range(1, len(self.labels)):
            print(
                f"{self.labels[label_index][0]} took"
                f"{self.labels[label_index][1] - self.labels[label_index - 1][1]: .3f} seconds")
        print('')

