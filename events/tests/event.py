from datetime import date, time 
from django.test import TestCase

from events.models import Event, Occurrence

# Fixture includes occurrences without events:
#
#   Pk: 1
#   Occurs: Feb 1, 2009
#   From:   6pm to 9pm
#
#   Pk: 2
#   Occurs: Everyday, from Feb 1st to Feb 10th
#   From:   8am to 2pm
#
#   Pk: 3
#   Occurs: Indefinitely, Every Tuesday
#   From:   8am to 2pm  
#
#   One general purpose event:
#       No Occurrences

class EventTests(TestCase):
    fixtures = ["occurrences", "events"]

    start = date(2009, 2, 1)
    end = date(2009, 2, 28)

    def test_event_should_lookup_in_all_occurrences(self):
        e = self.create_event(1, 3)
        dates = e.get_dates(self.start, self.end)
        self.destroy_event(e, 1, 3)

        self.assertEqual(len(dates), 5) 
        self.assertEqual([d.day for d in dates], [1, 3, 10, 17, 24])

    def test_event_should_not_have_duplicate_dates(self):
        e = self.create_event(1, 2)
        dates = e.get_dates(self.start, self.end)
        self.destroy_event(e, 1, 3)

        self.assertEqual(len(dates), 10)
        self.assertEqual([d.day for d in dates], [1,2,3,4,5,6,7,8,9,10])

    def test_event_is_in_range(self):
        e = Event.objects.get(pk = 1)
        self.associate_occurences(e, 1, 2)
        e = list(Event.objects.in_date_range(date(2009, 2, 1), date(2009, 2, 2)))
        self.dissociate_occurrences(1, 2)
        self.assertEqual(len(e), 1)

    def test_indefinite_event_is_in_range(self):
        e = Event.objects.get(pk = 1)
        self.associate_occurences(e, 1, 3)
        e = list(Event.objects.in_date_range(date(2009, 2, 3), date(2009, 2, 10)))
        self.dissociate_occurrences(1, 3)
        self.assertEqual(len(e), 1)

    def test_event_is_not_in_range(self):
        e = Event.objects.get(pk = 1)
        self.associate_occurences(e, 1)
        e = list(Event.objects.in_date_range(date(2009, 3, 1), date(2009, 3, 10)))
        self.dissociate_occurrences(1)
        self.assertEqual(len(e), 0)

# HELPERS
    def associate_occurences(self, event, *occurrences):
        for oid in occurrences:
            o = Occurrence.objects.get(pk=oid)
            o.event = event
            o.save()

    def dissociate_occurrences(self, *occurrences):
        for oid in occurrences:
            o = Occurrence.objects.get(pk = oid)
            o.event = None
            o.save()

    def create_event(self, *occurrences):
        e = Event(name="An Event")
        e.save()
        self.associate_occurences(e, *occurrences)
        return e

    def destroy_event(self, event, *occurrences):
        self.dissociate_occurrences(*occurrences)
        event.delete()
