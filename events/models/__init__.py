class _consts(object):   
    Single  = -1
    Daily   = 0
    Weekly  = 1
    Monthly = 2
    RecurrenceTypes = (
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

consts = _consts()

from event import Event
from recurrence import Recurrence
from occurrence import Occurrence
from category import Category
from venue import Venue

__all__ = ['Event', 'Occurrence', 'Venue','Category']
