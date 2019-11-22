import inspect
import json
import logging
import time
from pathlib import Path

root_path = Path(__file__).parent


def create_output_directory():
    Path(root_path/'data').mkdir(parents=True, exist_ok=True)


class Timer:
    def __init__(self):
        self.timed_methods = {}
        self.output_file = open(Path(root_path / 'data') / "timer.json", "w")
        self.start = None
        self.end = None

    def start_timer(self):
        self.start = time.process_time()

    def end_timer(self):
        self.end = time.process_time()
        caller = inspect.stack()[1][3]
        filename = Path(inspect.stack()[1][1]).name
        entry = filename + ";" + str(caller)
        if entry not in self.timed_methods:
            self.timed_methods[entry] = [{"duration": self.end - self.start}]
        else:
            self.timed_methods[entry].append({"duration": self.end - self.start})

    def __del__(self):
        result = json.dumps(self.timed_methods, indent=4)
        self.output_file.write(result)
        self.output_file.close()


create_output_directory()

t = Timer()
