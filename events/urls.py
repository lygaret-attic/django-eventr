from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    (r'^$', 'calendar'),
    (r'^(?P<year>\d{4})/$', 'calendar'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'calendar'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'calendar'),
)
