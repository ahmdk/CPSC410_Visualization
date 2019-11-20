import inspect
import json


class Frequency:
    """Logs the frequency of calls to particular functions in a given source code"""

    def __init__(self):
        self.function_frequency = {}
        self.output_file = open("function_count.json", "w")

    def count(self):
        "check which function you re being called from and increment that function's call frequency"
        caller = inspect.stack()[1][3]
        if self.function_frequency[caller] == None:
            self.function_frequency[caller] = 1
        else:
            self.function_frequency[caller] += 1

    def endCountLog(self):
        result = json.dumps(self.function_frequency, indent=4)
        self.output_file.write(result)
        self.output_file.close()


if __name__ == "__main__":
    f = Frequency()
    f.callerFunc()

