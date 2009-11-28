from django.db import models
from utils.fields import AutoSlugField, AutoMarkdownTextField

class BaseModel(models.Model):
    """
    A MixIn providing the basic name, slug (auto populated), description, and 
    markdown rendered description (auto populated) fields to django model objects.
    """
    name                = models.CharField(max_length=255, blank=False)
    slug                = AutoSlugField(prepopulate_from="name", unique=True, blank=True)

    description         = models.TextField(blank=True)
    description_html    = AutoMarkdownTextField(prepopulate_from="description", blank=True)

    date_created        = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified       = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
