from django.contrib import admin
from events.models import *

admin.site.register(Venue)
admin.site.register(Category)

class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [
            OccurrenceInline,
    ]

admin.site.register(Event, EventAdmin)
