from django.db import models
from events.models import consts
from utils.fields import SerializedDataField

class OccurrenceManager(models.Manager):
    def get_query_set(self):
        return super(OccurrenceManager, self).get_query_set()

    def get_in_dates(self, start, end):
        return self.filter(end__gte = start, end__lte = end) |\
               self.filter(start__gte = start, start__lte = end) |\
               self.filter(indefinite = True)

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
    event           = models.ForeignKey('Event', related_name='occurrences', null=True)

    objects         = OccurrenceManager()

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

        from events.models import Recurrence
        r = Recurrence.get_recurrence(self.recur_type, self.recur_values)
        return r.all_dates_in(dates[0], dates[1])

