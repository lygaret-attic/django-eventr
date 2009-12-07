from datetime import date, time
from django.test import TestCase

from events.models import Occurrence
from events.models import calendar

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
    window_four = [date(2009, 4, 13), date(2009, 4, 19)]

    expected_counts_window_one = [1, 10, 52, 26, 12, 6]
    expected_counts_window_two = [1, 10, 4, 8, 1, 0]
    expected_counts_window_three = [0, 0, 18, 0, 4, 6]
    expected_counts_window_four = [0, 0, 1, 2, 0, 0]

    expected_days_window_one = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    expected_days_window_two = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    expected_days_window_three = [2, 9, 16, 23, 30, 7, 14, 21, 28, 4]
    expected_days_window_four = [14,13,15]

    expected_months_window_one = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    expected_months_window_two = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    expected_months_window_three = [6, 6, 6, 6, 6, 7, 7, 7, 7, 8]
    expected_months_window_four = [4, 4, 4]

    def setUp(self):
        self.occurrences = Occurrence.objects.all()

    def get_date_counts(self, window):
        return [len(o.get_dates(window[0], window[1])) for o in self.occurrences]

    def get_date_days(self, window, count=10):
        return sum([[d.day for d in o.get_dates(window[0], window[1])] for o in self.occurrences], [])[:count]

    def get_date_months(self, window, count=10):
        return sum([[d.month for d in o.get_dates(window[0], window[1])] for o in self.occurrences], [])[:count]

    def test_expected_date_counts(self):
        self.assertEqual(self.get_date_counts(self.window_one), self.expected_counts_window_one)
        self.assertEqual(self.get_date_counts(self.window_two), self.expected_counts_window_two)
        self.assertEqual(self.get_date_counts(self.window_three), self.expected_counts_window_three)
        self.assertEqual(self.get_date_counts(self.window_four), self.expected_counts_window_four)
    
    def test_expected_date_days(self):
        self.assertEqual(self.get_date_days(self.window_one), self.expected_days_window_one)
        self.assertEqual(self.get_date_days(self.window_two), self.expected_days_window_two)
        self.assertEqual(self.get_date_days(self.window_three), self.expected_days_window_three)
        self.assertEqual(self.get_date_days(self.window_four), self.expected_days_window_four)

    def test_expected_date_months(self):
        self.assertEqual(self.get_date_months(self.window_one), self.expected_months_window_one)
        self.assertEqual(self.get_date_months(self.window_two), self.expected_months_window_two)
        self.assertEqual(self.get_date_months(self.window_three), self.expected_months_window_three)
        self.assertEqual(self.get_date_months(self.window_four), self.expected_months_window_four)

    def test_in_week_calendar(self):
        c = calendar.OneWeek(2009, 8, 3)
        dates = c.get_datemap()
        # we have occurrences on the 4th (two, pk = [3, 6]) and on the 7th (pk = 5)
        self.assertEqual(len(dates.keys()), 2)
        self.assertEqual(len(dates[date(2009, 8, 4)]), 2)
        self.assertEqual(len(dates[date(2009, 8, 7)]), 1)

    def test_in_month_calendar(self):
        c = calendar.OneMonth(2009, 8)
        dates = c.get_datemap()
        # we have occurrences on the 4th, 7th, 11th, 18th, 20th and the 25th
        days = [date(2009, 8, d) for d in [4, 7, 11, 18, 20, 25]]
        for d in days:
            self.assertTrue(len(dates[d]) > 0)

