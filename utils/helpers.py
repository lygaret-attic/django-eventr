from datetime import date
from dateutil.relativedelta import *

def daterange(start, end, **incr):
    incr = relativedelta(**incr)
    date = start
    while date <= end:
        yield date
        date = date + incr

def count(start, off):
    while True:
        yield start
        start += off

def uniquify(list):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for x in xs:
        marker = idfun(x)
        if marker in seen: continue
        seen[marker] = 1
        result.append(x)
    return result

