from django.shortcuts import render_to_response
from dateutil.parser import parse
from events.models import calendar

def _mon(month):
    return parse(month).month

def _dateview(request, cal, template):
    return render_to_response(template, { "calendar": cal })

def thisweek(request):
    return _dateview(request, calendar.ThisWeek(), 'events/event_page.html')

def oneyear(request, year):
    return _dateview(request, calendar.OneYear(int(year)), 'events/event_page.html')
    
def onemonth(request, year, month):
    return _dateview(request, calendar.OneMonth(int(year), _mon(month)), 'events/event_page.html')

def oneday(request, year, month, day):
    return _dateview(request, calendar.OneDay(int(year), _mon(month), int(day)), 'events/event_page.html')
