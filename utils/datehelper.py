from datetime import date
from dateutil.relativedelta import *

def daterange(start, end, **incr):
    incr = relativedelta(**incr)
    date = start
    while date <= end:
        yield date
        date = date + incr
