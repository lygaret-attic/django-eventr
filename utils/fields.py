from django.db.models import fields
from django.template.defaultfilters import slugify
from markdown import markdown

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

class AutoSlugField(fields.SlugField):
    def __init__(self, *args, **kwargs):
        if "prepopulate_from" in kwargs:
            self.prepopulate_from = kwargs["prepopulate_from"]
            del(kwargs["prepopulate_from"])
        else:
            self.prepopulate_from = False
        return super(AutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from and not model_instance.pk:
            base = getattr(model_instance, self.prepopulate_from)
            slug = slugify(base) 
            if self.unique:
                slug = unique_slug(model_instance.__class__, self.name, slug)
            setattr(model_instance, self.name, slug)
            return slug
        else:
            return super(AutoSlugField, self).pre_save(model_instance, add)

class AutoMarkdownTextField(fields.TextField):
    def __init__(self, *args, **kwargs):
        if "prepopulate_from" in kwargs:
            self.prepopulate_from = kwargs["prepopulate_from"]
            del(kwargs["prepopulate_from"])
        else:
            self.prepoulate_from = None
        return super(AutoMarkdownTextField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from:
            base = getattr(model_instance, self.prepopulate_from)
            text = markdown(base)
            setattr(model_instance, self.name, text)
            return text
        else:
            return super(AutoMarkdownTextField, self).pre_save(model_instance, add)

try:
    import cPickle as pickle
except ImportError:
    import pickle

class PickleDescriptor(property):
    def __init__(self, field):
        self.field = field

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value
        setattr(instance, self.field.attname, self.field.pickle(value))

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.field.name not in instance.__dict__:
            # The object hasn't been created yet, so unpickle the data
            raw_data = getattr(instance, self.field.attname)
            instance.__dict__[self.field.name] = self.field.unpickle(raw_data)

        return instance.__dict__[self.field.name]

class PickleField(fields.TextField):
    def pickle(self, obj):
        return pickle.dumps(obj)

    def unpickle(self, data):
        return pickle.loads(str(data))

    def get_attname(self):
        return "%s_pickled" % self.name

    def get_db_prep_lookup(self,lookup_type,value):
        raise ValueError("Can't make comparisons against pickled data.")

    def contribute_to_class(self, cls, name):
        super(PickleField, self).contribute_to_class(cls, name)
        setattr(cls, name, PickleDescriptor(self))
    
