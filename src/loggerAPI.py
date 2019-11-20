import inspect
import time
import json
import logging


def log():
    callstack = []
    for f in inspect.stack():
        callstack.append(f[3])
    logging.info("******************* Frame start ********************")
    logging.info("\n".join(callstack[1:]))
    logging.info("******************* Frame end   ********************")


def startlog():
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        format="%(asctime)s.%(msecs)03d \n%(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )


class Frequency:
    """Logs the frequency of calls to particular functions in a given source code"""

    def __init__(self):
        self.function_frequency = {}
        self.output_file = open("function_count.json", "w")

    def count(self):
        "check which function you re being called from and increment that function's call frequency"
        caller = inspect.stack()[1][3]
        if caller not in self.function_frequency:
            self.function_frequency[caller] = 1
        else:
            self.function_frequency[caller] += 1

    def endCountLog(self):
        result = json.dumps(self.function_frequency, indent=4)
        self.output_file.write(result)
        self.output_file.close()

    def __del__(self):
        self.endCountLog()


f = Frequency()
