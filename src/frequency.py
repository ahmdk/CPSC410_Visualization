import inspect


class Frequency:
    """Logs the frequency of calls to particular functions in a given source code"""

    def __init__(self):
        self.function_frequency = {}

    def count(self):
        "check which function you re being called from and increment that function's call frequency"
        caller = inspect.stack()[1][3]
        print(caller)
        self.function_frequency[caller]

    def callerFunc(self):
        self.count()
        print(self.function_frequency)


if __name__ == "__main__":
    f = Frequency()
    f.callerFunc()

