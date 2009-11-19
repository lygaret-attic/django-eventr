from django.contrib import admin
from events.models import *

admin.site.register(Venue)
admin.site.register(Category)

class OccuranceInline(admin.TabularInline):
    model = Occurance
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [
            OccuranceInline,
    ]

admin.site.register(Event, EventAdmin)
