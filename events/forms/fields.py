from events.models import Recurrence
from utils import forms as utilforms

class RecurrenceField(utilforms.JSONField):
    """
    A field which inserts a recurrence type and recurrence 
    values (as a tuple) into cleaned_data.
    """
    def __init__(self, *args, **kwargs):
        super(RecurrenceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(RecurrenceField, self).clean(value)

        # try creating a recurrence
        try:
            r = Recurrence.get_recurrence(value['type'], value['values'])
        except:
            raise ValidationError(self.error_messages['invalid'])

        return (value['type'], value['values'])

