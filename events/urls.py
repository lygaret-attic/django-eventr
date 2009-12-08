from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    (r'^$', 'thisweek'),
    (r'^(?P<year>\d{4})/$', 'oneyear'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'onemonth'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', 'oneday'),
)
