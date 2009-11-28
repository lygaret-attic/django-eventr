from django.db import models
from utils import fields

class TestAutoDescriptionModel(models.Model):
    text = models.TextField()
    html = fields.AutoMarkdownTextField(prepopulate_from = "text")
    nonpop = fields.AutoMarkdownTextField()

class TestAutoSlugModel(models.Model):
    name = models.CharField(max_length = 255)
    slug = fields.AutoSlugField(prepopulate_from = "name", unique = False)
    uniq = fields.AutoSlugField(prepopulate_from = "name", unique = True)
    nonpop = fields.AutoSlugField()

class TestSerializedDataModel(models.Model):
    data = fields.SerializedDataField(null = True)
