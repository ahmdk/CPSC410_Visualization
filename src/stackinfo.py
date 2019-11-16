import inspect
import time
import json
from   collections import defaultdict

class Log:
    stackinfo = defaultdict(list)
    output_file = open("output.json", "w")
    start_time = 0
    
    @staticmethod
    def log():
        caller  = inspect.stack()[2][3]
        current = inspect.stack()[1][3]
        Log.stackinfo[caller].append((str(time.time() - Log.start_time), current))
    
    @staticmethod
    def start_log():
        Log.start_time = time.time()
    
    @staticmethod
    def end_log():
        # sort function calls in chronological order
        # output = sorted(Log.stackinfo.iteritems(), key=lambda(k,v): v[0][0], reverse = False)
        result = json.dumps(Log.stackinfo, indent=4, sort_keys = True)
        Log.output_file.write(result)
        Log.output_file.close()
