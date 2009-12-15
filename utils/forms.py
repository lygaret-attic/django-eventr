from django import forms
from django.utils import simplejson

class JSONField(forms.CharField):
    """ 
    Allow posting JSON to and from a form field. It will validate
    as JSON and return a parsed dictionary in cleaned_data.
    """
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(JSONField, self).clean(value)
        try:
            data = simplejson.loads(value)
        except:
            raise ValidationError(self.error_messages['invalid'])
        return data
