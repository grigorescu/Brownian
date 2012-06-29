from django import template
from django.conf import settings
import datetime
import pytz

register = template.Library()

def dateToDatetime(value):
    """Converts milliseconds since epoch that ElasticSearch uses to Python Datetime object."""
    if not value:
        return ""
    date = datetime.datetime.utcfromtimestamp(float(str(value))/1000)
    return pytz.utc.localize(date).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%a %b %d %H:%M:%S.%f')[:-3]

register.filter("dateToDatetime", dateToDatetime)