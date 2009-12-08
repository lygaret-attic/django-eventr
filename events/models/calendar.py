from events.models import *
from datetime import date
from dateutil.relativedelta import *
from collections import defaultdict
from utils.helpers import daterange

class Calendar(object):
    """
    A calendar is a utility which returns a set of occurrences corresponding 
    to a particular set of dates. This is subclassed to provide standard
    time periods (next 7 days, this month, etc.)
    """

    @staticmethod
    def trim_to(calendar, **delta):
        end = calendar.start + relativedelta(**delta)
        return Calendar(calendar.start, end)

    def __init__(self, start, end):
        super(Calendar, self).__init__()
        self.start = start
        self.end = end

    def get_alldates(self):
        return list(daterange(self.start, self.end, days=+1))

    def get_occurrences(self):
        os = Occurrence.objects.get_in_dates(self.start, self.end).select_related('event')
        occurrences = []
        for o in os:
            if len(o.get_dates(self.start, self.end)) > 0:
                occurrences.append(o)

        return occurrences

    def get_datemap(self):
        datemap = defaultdict(list)
        for o in self.get_occurrences():
            for d in o.get_dates(self.start, self.end):
                datemap[d].append(o)
        return datemap

    def __iter__(self):
        datemap = self.get_datemap()
        datelist = self.get_alldates()
        for day in datelist:
            yield CalendarDay(day, datemap[day])

class CalendarDay(object):
    """
    A container class for a particular date, and a given list of occurrences.
    This class should only ever be created by a Calendar object.
    """
    def __init__(self, date, occurrences):
        self.date = date
        self.occurrences = occurrences

class OneDay(Calendar):
    def __init__(self, year, month, day):
        start = date(year, month, day)
        super(OneDay, self).__init__(start, start)

class OneWeek(Calendar):
    def __init__(self, year, month, day):
        start = date(year, month, day)
        super(OneWeek, self).__init__(start, start + relativedelta(days=+6))

class OneMonth(Calendar):
    def __init__(self, year, month):
        start = date(year, month, 1)
        end   = start + relativedelta(months=+1) + relativedelta(days=-1)
        super(OneMonth, self).__init__(start, end)

class OneYear(Calendar):
    def __init__(self, year):
        start = date(year, 1, 1)
        end   = date(year, 12, 31)
        super(OneYear, self).__init__(start, end)

class ThisWeek(OneWeek):
    def __init__(self):
        today = date.today() + relativedelta(days = -1)
        super(ThisWeek, self).__init__(today.year, today.month, today.day)

class ThisMonth(OneMonth):
    def __init__(self):
        today = date.today()
        super(ThisMonth, self).__init__(today.year, today.month)

