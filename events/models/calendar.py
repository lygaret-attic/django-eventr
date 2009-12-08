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

    def __init__(self, start, end):
        super(Calendar, self).__init__()
        self.start = start
        self.end = end

    def get_alldates(self):
        return list(daterange(self.start, self.end, days=+1))

    def get_occurrences(self):
        os = Occurrence.objects.filter(start__lte = self.start, end__gte = self.end) |\
             Occurrence.objects.filter(indefinite = True)
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

class OneWeek(Calendar):
    def __init__(self, year, month, day):
        start = date(year, month, day)
        super(OneWeek, self).__init__(start, start + relativedelta(days=+7))

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
        today = date.today()
        super(ThisWeek, self).__init__(today.year, today.month, today.day)

class ThisMonth(OneMonth):
    def __init__(self):
        today = date.today()
        super(ThisMonth, self).__init__(today.year, today.month)

