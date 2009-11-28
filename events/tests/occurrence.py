from datetime import date, time

from django.test import TestCase
from events.models import Occurrence

# FIXTURE INCLUDES
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
#   Pk: 4
#   Occurs: From Feb through April, Every Monday and Wednesday
#   From:   8pm to 11pm
#
#   Pk: 5
#   Occurs: Indefinitely, Every 1st Friday
#   From:   6pm to Midnight
#
#   Pk: 6
#   Occurs: From June to August, Every 1st Tuesday and 3rd Thursday
#   From:   7pm to Midnight

class OccurrenceTests(TestCase):
    fixtures = ["occurrences"]

    window_one = [date(2009,1,1), date(2009,12,31)]
    window_two = [date(2009,2,1), date(2009,2,28)]
    window_three = [date(2009,6,1), date(2009,9,30)]

    expected_counts_window_one = [1, 10, 52, 26, 12, 6]
    expected_counts_window_two = [1, 10, 4, 8, 1, 0]
    expected_counts_window_three = [0, 0, 18, 0, 4, 6]

    def setUp(self):
        self.occurrences = Occurrence.objects.all()

    def get_date_counts(self, window):
        return [len(o.get_dates(window[0], window[1])) for o in self.occurrences]

    def test_expected_date_counts(self):
        self.assertEqual(self.get_date_counts(self.window_one), self.expected_counts_window_one)
        self.assertEqual(self.get_date_counts(self.window_two), self.expected_counts_window_two)
        import pdb
        pdb.set_trace()
        self.assertEqual(self.get_date_counts(self.window_three), self.expected_counts_window_three)
    
