from django import template
import datetime

register = template.Library()

def dateToDatetime(value):
    """Converts milliseconds since epoch that ElasticSearch uses to Python Datetime object."""
    if not value:
        return ""
    return datetime.datetime.utcfromtimestamp(float(str(value))/1000).strftime('%a %b %d %H:%M:%S.%f')[:-3]

register.filter("dateToDatetime", dateToDatetime)