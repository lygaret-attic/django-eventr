from django import template

register = template.Library()

@register.filter
def hash(value, key):
    " Returns value[key] "
    return value[key]

@register.filter
def cssclasses(calendarday, orig):
    " Returns css classes for a particular date "
    css = [orig]
    if calendarday.date.weekday() in [5, 6]:
        css.append("weekend")
    if len(calendarday.occurrences) > 0:
        css.append("events")
    return " ".join(css)
