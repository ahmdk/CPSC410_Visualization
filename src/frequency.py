import inspect


class Frequency:
    """Logs the frequency of calls to particular functions in a given source code"""

    def __init__(self):
        self.function_frequency = {}

    def count(self):
        "check which function you re being called from and increment that function's call frequency"
        caller = inspect.stack()[2][3]
        self.function_frequency[caller] += 1


if __name__ == "__main__":
    f = Frequency()
    f.count()

