from django.shortcuts import render_to_response

from collections import defaultdict
from datetime import date
from dateutil.relativedelta import *
from utils.helpers import daterange
from events.models import Event
from events.models import calendar

minus_one_day = relativedelta(days=-1)
plus_one_week = relativedelta(days=+6)

def _gen_dates():
    startdate = startdate if startdate else (date.today() + minus_one_day)
    enddate = startdate + plus_one_week
    return (startdate, enddate)

def _dateview(request, cal, template):
    days   = cal.get_alldates()
    events = cal.get_eventmap()
    import pdb
    pdb.set_trace()
    return render_to_response(template, locals())

def thisweek(request):
    return _dateview(request, calendar.ThisWeek(), 'events/week_calendar.html')

def oneyear(request, year):
    return _dateview(request, calendar.OneYear(int(year)), 'events/week_calendar.html')
    
def onemonth(request, year, month):
    return _dateview(request, calendar.OneMonth(int(year), int(month)), 'events/week_calendar.html')

def oneweek(request, year, month, dat):
    return _dateview(request, calendar.OneWeek(year, month, day), 'events/week_calendar.html')
