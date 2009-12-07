from django.db import models
from utils.models import BaseModel
from utils.helpers import uniquify

from occurrence import Occurrence
from category import Category
from venue import Venue

class EventManager(models.Manager):
    def in_date_range(self, start, end):
        explicit = self.filter(occurrences__start__gte=start, occurrences__end__lte=end)
        implicit = self.filter(occurrences__indefinite=True)
        return (explicit | implicit).select_related()

class Event(BaseModel):
    """
    An event is the definition of the event, along with references out to
    the various pieces of data and a set of occurances.
    """
    cost        = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    free        = models.BooleanField()
    venue       = models.ForeignKey(Venue, null=True, blank=False)
    categories  = models.ManyToManyField(Category)
    approved    = models.BooleanField()

    objects     = EventManager()

    class Meta:
        app_label = 'events'

    def get_dates(self, start=None, end=None):
        dates = []
        for o in self.occurrences.all():
            for d in o.get_dates(start, end):
                dates.append(d)
        return uniquify(dates)

