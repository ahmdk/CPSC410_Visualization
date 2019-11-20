from frequency import Frequency  # inject at import section

f = Frequency()  # inject before first function def

# inject at f.count() at every function definition in the codebase
def function1():
    f.count()


def function2():
    f.count()


def function3():
    f.count()


function1()
function2()
function3()
function2()

f.endCountLog()  # inject at end of file
