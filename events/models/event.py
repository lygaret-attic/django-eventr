from django.db import models
from utils.models import BaseModel
from utils.fields import SerializedDataField
from events.models import consts, Recurrence

from category import Category
from venue import Venue

def _uniquify(xs, idfun=None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for x in xs:
        marker = idfun(x)
        if marker in seen: continue
        seen[marker] = 1
        result.append(x)
    return result

class Event(BaseModel):
    """
    An event is the definition of the event, along with references out to
    the various pieces of data and a set of occurances.
    """
    cost        = models.DecimalField(decimal_places=2, max_digits=7, blank=True)
    free        = models.BooleanField()
    venue       = models.ForeignKey(Venue)
    categories  = models.ManyToManyField(Category)
    approved    = models.BooleanField()

    class Meta:
        app_label = 'events'

    def get_dates(self, start=None, end=None):
        dates = []
        for o in self.occurrences.all():
            for d in o.get_dates(start, end):
                dates.append(d)
        return _uniquify(dates)

class Occurrence(models.Model):
    """
    An occurrence is a definition of a specific range of dates during which
    an event can take place. It can be a single date range or a recurring
    pattern of dates taking place between two dates.
    """
    start           = models.DateField(blank = True, null = True)
    end             = models.DateField(blank = True, null = True)
    indefinite      = models.BooleanField()
    starttime       = models.TimeField()
    endtime         = models.TimeField()
    recur_type      = models.IntegerField(choices=consts.RecurrenceTypes, blank=True, null=True)
    recur_values    = SerializedDataField(blank=True, null=True)

    event           = models.ForeignKey(Event, related_name='occurrences', null=True)

    class Meta:
        app_label = 'events'

    def get_border_dates(self, start, end):
        if not self.indefinite:
            if start < self.start: start = self.start
            if end > self.end: end = self.end
        return (start, end)

    def get_dates(self, start, end):
        dates = self.get_border_dates(start, end)

        if self.recur_type == consts.Single:
            if self.start >= start and self.end <= end:
                return [dates[0]]
            else:
                return []

        r = Recurrence.get_recurrence(self.recur_type, self.recur_values)
        return r.all_dates_in(dates[0], dates[1])
