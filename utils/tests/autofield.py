from django.test import TestCase
from django.db import models
from utils import fields
from utils.tests.models import *

incoming_markdown = "**bold**, *italic*"
gen_html = "<p><strong>bold</strong>, <em>italic</em></p>"

class AutoMarkdownTests(TestCase):
    def setUp(self):
        self.m = TestAutoDescriptionModel()
        self.m.text = incoming_markdown
        self.m.save()

    def tearDown(self):
        self.m.delete()

    def test_nonpop_markdown(self):
        self.assertEquals(self.m.nonpop, "")

    def test_auto_markdown(self):
        self.assertEquals(self.m.html, gen_html)

class AutoSlugTests(TestCase):
    
    def setUp(self):
        self.m1 = TestAutoSlugModel(name = "Some String")
        self.m1.save()
        self.m2 = TestAutoSlugModel(name = "Some String")
        self.m2.save()
        super(AutoSlugTests, self).setUp()

    def tearDown(self):
        self.m1.delete()
        self.m2.delete()

    def test_nongen_slug(self):
        m = TestAutoSlugModel(name = "Some String")
        m.slug = "a-slug"
        m.uniq = "a-slug"
        m.save()
        self.assertEquals(m.name, "Some String")
        self.assertEquals(m.slug, "a-slug")
        self.assertEquals(m.uniq, "a-slug")

    def test_nonpop_slug(self):
        self.assertEquals(self.m1.nonpop, "")
    
    def test_nonuniq_slug(self):
        self.assertEquals(self.m1.slug, "some-string")
        self.assertEquals(self.m2.slug, "some-string")

    def test_uniq_slug(self):
        self.assertEquals(self.m1.uniq, "some-string")
        self.assertEquals(self.m2.uniq, "some-string-1")

class SerializedDataTests(TestCase):

    def setUp(self):
        self.list = TestSerializedDataModel()
        self.list.data = [1,2,3,4,5,6,7,8,9]
        self.list.save()

        self.tuples = TestSerializedDataModel()
        self.tuples.data = (1,2,3)
        self.tuples.save()

    def test_serialized(self):
        l = TestSerializedDataModel.objects.get(pk = 1)
        self.assertEquals(type(l.data), type([1]))
        self.assertEquals(l.data, [1,2,3,4,5,6,7,8,9])

        t = TestSerializedDataModel.objects.get(pk = 2)
        self.assertEquals(type(t.data), type((1,)))
        self.assertEquals(t.data, (1,2,3))
