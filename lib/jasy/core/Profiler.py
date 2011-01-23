#
# Jasy - JavaScript Tooling Refined
# Copyright 2010 Sebastian Werner
#

import time, logging

__all__ = ["pstart", "pstop"]

__start = None
__enabled = True

def penable():
    global __enabled
    __enabled = True
    
def pdisable():
    global __enabled
    __enabled = False

def pstart():
    global __start
    global __enabled

    if __enabled:
        __start = time.time()
    
    
def pstop():
    global __start
    global __enabled

    if __enabled:
        now = time.time()
        logging.info(" - in %sms" % int((now-__start)*1000))
        __start = now
    