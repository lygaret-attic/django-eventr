from django.test import TestCase
from datetime import date, timedelta

import events.models as consts
from events.models.recurrence import *

class RecurrenceTests(TestCase):

    def setUp(self):
        self.start = date(2009,2,1)
        self.oneweek = date(2009,2,8)
        self.onemonth = date(2009,3,1)
        self.threemonths = date(2009,5,1)

    def test_recurrence_factory_to_get_daily(self):
        r = Recurrence.get_recurrence(consts.Daily)
        d = DailyRecurrence()
        self.assertEqual(type(r), type(d))

    def test_recurrence_factory_to_get_monthly(self):
        r = Recurrence.get_recurrence(consts.Monthly)
        m = MonthlyRecurrence([])
        self.assertEqual(type(r), type(m))

    def test_factory_raises(self):
        self.assertRaises(ValueError, Recurrence.get_recurrence, 9)
        self.assertRaises(ValueError, Recurrence.get_recurrence, consts.Monthly, ['hi'])

    def test_daily_recurrence(self):
        r = Recurrence.get_recurrence(consts.Daily)
        dates = r.all_dates_in(self.start, self.oneweek)
        self.assertEqual(len(dates), 8)
        self.assertEqual(dates[2].day, 3)
        self.assertEqual(dates[5].day, 6)

    def test_weekly_recurrence(self):
        r = Recurrence.get_recurrence(consts.Weekly, [consts.Monday, consts.Friday])
        dates = r.all_dates_in(self.start, self.oneweek)
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0].day, 2) # feb 2 is monday
        self.assertEqual(dates[1].day, 6) # feb 6 is friday

    def test_weekly_again(self):
        r = Recurrence.get_recurrence(consts.Weekly, [consts.Monday, consts.Tuesday, consts.Sunday])
        dates = r.all_dates_in(self.start, self.onemonth)
        self.assertEqual(len(dates), 12)
        self.assertEqual(dates[11].day, 24) # last tuesday in feb

    def test_monthly_recurrence(self):
        r = Recurrence.get_recurrence(consts.Monthly, [7, 10, (consts.Friday, 1)])
        dates = r.all_dates_in(self.start, self.threemonths)
        self.assertEqual(len(dates), 9)
        self.assertEqual([6,7,10,6,7,10,3,7,10], [d.day for d in dates])
        self.assertEqual([2,2,2,3,3,3,4,4,4], [d.month for d in dates])
