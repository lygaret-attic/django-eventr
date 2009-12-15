class _consts(object):   
    Single  = -1
    Daily   = 0
    Weekly  = 1
    Monthly = 2
    RecurrenceTypes = (
        (Single, "No Recurrence"),
        (Daily, "Daily"),
        (Weekly, "Weekly"),
        (Monthly, "Monthly"),
    )

    Monday      = 0
    Tuesday     = 1
    Wednesday   = 2
    Thursday    = 3
    Friday      = 4
    Saturday    = 5
    Sunday      = 6
    RecurrenceWeekdays = (
        (Monday, "Monday"),
        (Tuesday, "Tuesday"),
        (Wednesday, "Wednesday"),
        (Thursday, "Thursday"),
        (Friday, "Friday"),
        (Saturday, "Saturday"),
        (Sunday, "Sunday"),
    )

    First       = 1
    Second      = 2
    Third       = 3
    Fourth      = 4
    Fifth       = 5
    RecurrenceInstances = (
        (First, "First"),
        (Second, "Second"),
        (Third, "Third"),
        (Fourth, "Fourth"),
        (Fifth, "Fifth"),
    )

consts = _consts()

from event import Event
from recurrence import Recurrence
from occurrence import Occurrence
from category import Category
from venue import Venue

__all__ = ['Event', 'Occurrence', 'Venue','Category']
