from django.test import TestCase
from datetime import date, datetime
from events.models import *
from events.models import consts

class EventTests(TestCase):
    fixtures = ["event_testdata"]
    
    def setUp(self):
        self.recurring_event = Event.objects.all()[0]
        self.start_date = datetime(2010, 02, 01)
        self.end_date = datetime(2010, 03, 30)

    def test_event_dates(self):
        dates = self.recurring_event.get_dates(self.start_date, self.end_date)
        self.assertEqual(3, len(dates))
