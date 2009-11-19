from django.db import models
from utils.fields import AutoSlugField
from utils.models import BaseModel

class Venue(BaseModel):
    """
    A venue is a location where an event can take place.
    A Venue contains identifying and contact information for a particular location.
    """
    link        = models.URLField()
    email       = models.EmailField()
    phone       = models.CharField(max_length=16)

    address1    = models.CharField(max_length=255, blank=False)
    address2    = models.CharField(max_length=255, blank=True, default="")
    city        = models.CharField(max_length=255, blank=False)
    state       = models.CharField(max_length=100, blank=False)
    zip         = models.CharField(max_length=10, blank=False)

    class Meta:
        app_label = 'events'
        ordering = ('name',)

    def __unicode__(self):
        return self.name
