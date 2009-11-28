from django.db.models import fields, SubfieldBase
from django.template.defaultfilters import slugify
from markdown import markdown
import pickle
import base64

class AutoSlugField(fields.SlugField):
    """
    A slug field which can be automatically generated, assuming no slug
    has been given to the model prior to saving. If you assign a slug during
    or after creation, that is the slug that will be used.
    """
    @staticmethod
    def unique_slug(model, slug_field, slug_value):
        index = 0
        orig_slug = slug_value
        while True:
            try:
                model.objects.get(**{slug_field:slug_value})
            except model.DoesNotExist:
                return slug_value
            index += 1
            slug_value = orig_slug + '-' + str(index)

    def __init__(self, *args, **kwargs):
        if "prepopulate_from" in kwargs:
            self.prepopulate_from = kwargs["prepopulate_from"]
            del(kwargs["prepopulate_from"])
        else:
            self.prepopulate_from = False
        return super(AutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from and not model_instance.pk and not getattr(model_instance, self.name):
            base = getattr(model_instance, self.prepopulate_from)
            slug = slugify(base) 
            if self.unique:
                slug = AutoSlugField.unique_slug(model_instance.__class__, self.name, slug)
            setattr(model_instance, self.name, slug)
            return slug
        else:
            return super(AutoSlugField, self).pre_save(model_instance, add)

class AutoMarkdownTextField(fields.TextField):
    """
    A field which auto populates with the value of the given field, 
    processed through markdown. This field will _always_ repopulate
    if the value of prepopulate_from is set.
    """
    def __init__(self, *args, **kwargs):
        if "prepopulate_from" in kwargs:
            self.prepopulate_from = kwargs["prepopulate_from"]
            del(kwargs["prepopulate_from"])
        else:
            self.prepopulate_from = None
        return super(AutoMarkdownTextField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from:
            base = getattr(model_instance, self.prepopulate_from)
            text = markdown(base)
            setattr(model_instance, self.name, text)
            return text
        else:
            return super(AutoMarkdownTextField, self).pre_save(model_instance, add)


class SerializedDataField(fields.TextField):
    """
    A field which serializes python values to the database, and returns
    them intact.
    """
    __metaclass__ = SubfieldBase

    def to_python(self, value):
        if value is None or value is "": return
        if not isinstance(value, basestring): return value
        return pickle.loads(base64.b64decode(value))

    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))
