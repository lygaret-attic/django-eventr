from django.shortcuts import render_to_response

from collections import defaultdict
from datetime import date
from dateutil.relativedelta import *
from utils.helpers import daterange
from events.models import Event

minus_one_day = relativedelta(days=-1)
plus_one_week = relativedelta(days=+6)

def gen_week_dates(startdate):
    startdate = startdate if startdate else (date.today() + minus_one_day)
    enddate = startdate + plus_one_week
    return (startdate, enddate)

from functools import wraps
def parsedates():
    def inner_parse_dates(fn):
        def wrapped(request, year=None, month=None, day=None):
            if year is None:
                return fn(request, startdate = date.today())
            elif month is None:
                return fn(request, startdate = date(int(year), 1, 1))
            elif day is None:
                return fn(request, startdate = date(int(year), int(month), 1))
            else:
                return fn(request, startdate = date(int(year), int(month), int(day)))
        return wraps(fn)(wrapped)
    return inner_parse_dates

@parsedates()
def calendar(request, startdate = None):
    start, end = gen_week_dates(startdate)
    all_events = Event.objects.in_date_range(start, end)

    days    = list(daterange(start, end, days=+1))
    events  = defaultdict(list)
    for d in days:
        for e in all_events:
            if len(e.get_dates(d, d)) > 0:
                events[d].append(e)

    return render_to_response('events/week_calendar.html', locals())
