import inspect
import json
import logging
from pathlib import Path

root_path = Path(__file__).parent


def create_output_directory():
    Path(root_path/'data').mkdir(parents=True, exist_ok=True)


def log():
    callstack = []
    for f in inspect.stack():
        callstack.append(f[3])
    logging.info("******************* Frame start ********************")
    logging.info("\n".join(callstack[1:]))
    logging.info("******************* Frame end   ********************")


def startlog():
    logging.basicConfig(
        filename=Path(root_path/'data') / "output.txt",
        filemode="w",
        format="%(asctime)s.%(msecs)03d \n%(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )


class Frequency:
    """Logs the frequency of calls to particular functions in a given source code"""

    def __init__(self):
        self.function_frequency = {}
        self.output_file = open(Path(root_path/'data') / "function_count.json", "w")

    def count(self):
        "check which function you re being called from and increment that function's call frequency"
        filename = inspect.stack()[1][1]
        caller = inspect.stack()[1][3]
        entry = str(filename) + ";" + str(caller)
        if entry not in self.function_frequency:
            self.function_frequency[entry] = 1
        else:
            self.function_frequency[entry] += 1

    def endCountLog(self):
        result = json.dumps(self.function_frequency, indent=4)
        self.output_file.write(result)
        self.output_file.close()

    def __del__(self):
        self.endCountLog()


create_output_directory()

f = Frequency()
