from django import template
from events.models.calendar import Calendar

register = template.Library()

@register.inclusion_tag('calendar/week.html')
def show_week(calendar):
    return { 'calendar': calendar }

@register.inclusion_tag('calendar/month.html')
def show_month(calendar):
    return { 'calendar': Calendar.trim_to(calendar, month = 1) }
