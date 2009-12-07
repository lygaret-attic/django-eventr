from datetime import date, timedelta
from dateutil.relativedelta import *
from django.db import models
from django.db.models import Q

from events.models import consts

D_WEEKLY  = timedelta(weeks=1)
D_DAILY   = timedelta(1)

def _count(start, off):
    while True:
        yield start
        start += off

class Recurrence(object):
    """
    A recurrence gives you a list of dats matching some pattern.
    """
    @staticmethod
    def get_recurrence(type, days=[]):
        """ Factory method for getting the right kind of recurrence. """
        if type == consts.Daily:
            return DailyRecurrence()
        elif type == consts.Weekly:
            return WeeklyRecurrence(days)
        elif type == consts.Monthly:
            return MonthlyRecurrence(days)
        else:
            raise ValueError("Bad recurrence type!")

    def all_dates_in(self, start, end):
        return list(self.dates_in(start, end))

class DailyRecurrence(Recurrence):
    """ Recurs every day during the requested period """
    def dates_in(self, start, end):
        # plus one is to make the recurrence inclusive
        for i in range(0, (end - start).days + 1):
            yield start + (D_DAILY * i)

class WeeklyRecurrence(Recurrence):
    """ 
    Recurs weekly, on the given weekdays. Weekdays are supplied in the
    constructor as a list of integers, 0 = Monday, 1 = Tuesday, ...
    """
    def __init__(self, days):
        self.days = days

    def dates_in(self, start, end):
        offsets = [timedelta((d - start.weekday()) % 7) for d in self.days]
        offsets.sort()
        for m in _count(0,1):
            for offset in offsets:
                d = start + (offset + (D_WEEKLY * m))
                if d >= end:
                    return
                yield d

class MonthlyRecurrence(Recurrence):
    """
    Recurs monthly, on the given days and pattern days. The days supplied should be
    either integers, giving the explicit day (5 = the 5th, etc.) or tuples of a weekday
    and the instance of that weekday ((consts.Monday, 3) = third monday of the month)
    """
    def __init__(self, days):
        self.explicit = []
        self.implicit = []
        for d in days:
            if type(d) is int:
                self.explicit.append(d)
            elif type(d) is tuple and len(d) == 2:
                self.implicit.append(d)
            else:
                raise ValueError

    def dates_in(self, start, end):
        exp_offsets = [timedelta(d - start.day) for d in self.explicit]
        
        for m in _count(0,1):
            month_begin = date(start.year, start.month, 1) + relativedelta(months=+m)

            offsets = list(exp_offsets)
            for imp in self.implicit:

                # offset calc: (example, 2nd tuesday)
                # (imp[0] - month_begin.weekday()) % 7 = number of days from start of month is the first
                # .. + (7 * (imp[1] - 1)) = number of weeks to go forward

                imp_offset = timedelta(((imp[0] - month_begin.weekday()) % 7) + (7 * (imp[1] - 1)))
                if (month_begin + imp_offset).month == month_begin.month:
                    offsets.append(imp_offset)
            offsets.sort()

            for offset in offsets:
                d = month_begin + offset
                if d < start or d >= end:
                    return
                yield d

