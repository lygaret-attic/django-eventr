from django.db import models
from events.models import consts
from utils.fields import SerializedDataField

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
