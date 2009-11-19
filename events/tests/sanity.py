from django.test import TestCase

class SanityTests(TestCase):
    def testThatIAmSane(self):
        self.assertEquals(1, 1)
