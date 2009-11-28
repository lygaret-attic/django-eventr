from django.test import TestCase
from datetime import date, datetime
from events.models import *
from events.models import consts


class EventTests(TestCase):
    fixtures = ["events"]
    
    def setUp(self):
        self.recurring_event = Event.objects.all()[0]
        self.start_date = datetime(2010, 02, 01)
        self.end_date = datetime(2010, 03, 30)

