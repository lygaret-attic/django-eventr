from django import forms
from django.forms import extras
from django.forms import formsets

from utils import forms as utilforms
from events.models import *
from events.forms.fields import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue

class EventForm(forms.Form):
    submitter_name      = forms.CharField(max_length = 255)
    submitter_email     = forms.EmailField()
    submitter_message   = forms.CharField(widget = forms.Textarea(), required = False)

    name                = forms.CharField(max_length = 255)
    description         = forms.CharField(widget = forms.Textarea(), required = False)
    venue               = forms.ModelChoiceField(queryset = Venue.objects.all(), required = False)
    categories          = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), required = False)

class OccurrenceForm(forms.Form):

    date            = forms.DateField(widget = extras.SelectDateWidget())
    start           = forms.TimeField()
    end             = forms.TimeField()

    recurrence      = RecurrenceField(widget = forms.Textarea())

OccurrenceFormset = formsets.formset_factory(OccurrenceForm, extra = 2)
