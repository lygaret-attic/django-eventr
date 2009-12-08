from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    (r'^$', 'thisweek'),
    (r'^(?P<year>\d{4})/$', 'oneyear'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'onemonth'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'oneday'),
)
