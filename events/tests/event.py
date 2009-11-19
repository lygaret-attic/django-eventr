from django.test import TestCase
from events.models import *
from events.models import consts

class EventTests(TestCase):
    fixtures = ["event_testdata"]

    def testFixtureSanity(self):
        self.assertEquals(Event.objects.count(), 1)
