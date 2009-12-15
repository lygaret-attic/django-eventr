import logging as log
from django.http import *
from django.shortcuts import render_to_response
from dateutil.parser import parse
from events.models import calendar
from events import forms

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

def new_event(request):
    if request.method == "POST":
        event_form = forms.EventForm(request.POST, prefix = 'event')
        occur_forms = forms.OccurrenceFormset(request.POST, prefix = 'occurs')

        if event_form.is_valid() and occur_forms.is_valid():
            log.debug(event_form.cleaned_data)
            log.debug(occurs_forms.cleaned_data)
            return HttpResponseRedirect('/')
    else:
        event_form = forms.EventForm(prefix = 'event')
        occur_forms = forms.OccurrenceFormset(prefix = 'occurs')

    return render_to_response('events/event_new.html', {'event_form': event_form, 'occur_forms': occur_forms})
