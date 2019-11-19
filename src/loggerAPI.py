import inspect
import time
import json
import logging

def log():
    callstack = []
    for f in inspect.stack():
        callstack.append(f[3])
    logging.info('******************* Frame start ********************')
    logging.info('\n'.join(callstack[1:]))
    logging.info('******************* Frame end   ********************')

def startlog():
    logging.basicConfig(
        filename="output.txt", filemode='w',             \
        format='%(asctime)s.%(msecs)03d \n%(message)s',  \
        datefmt='%H:%M:%S', level=logging.INFO)