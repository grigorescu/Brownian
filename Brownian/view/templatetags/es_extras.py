from django import template
from django.conf import settings
import datetime
import pytz

register = template.Library()

@register.filter(name='dateToDatetime')
def dateToDatetime(value):
    """Converts milliseconds since epoch that ElasticSearch uses to Python Datetime object."""
    if not value:
        return ""
    date = datetime.datetime.utcfromtimestamp(float(str(value))/1000)
    return pytz.utc.localize(date).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%a %b %d %H:%M:%S.%f')[:-3]

@register.filter(name='tsRange')
def tsRange(ts, value):
    """Converts timestamp to range[ts - value TO ts + value] with value in millis."""
    if not value or not ts:
        return ""

    time = int(ts)
    val = int(value)

    return "[%d TO %d]" % (time - val, time + val)

def genPagination(parser, token):
    """Generates pagination given the current location, and the total number of items."""

    try:
        tokens = token.split_contents()
        tag_name = tokens[0]
        start = tokens[1]
        total = tokens[2]
        openTab = tokens[3]
        query = tokens[4]
        indices = tokens[5]
        sortField = tokens[6]
        sortOrder = tokens[7]
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments (location, total, openTab, query, indices, sortField, sortOrder)." % tag_name)

    return Paginate(start, total, openTab, query, indices, sortField, sortOrder)

class Paginate(template.Node):
    def __init__(self, start, total, openTab, query, indices, sortField, sortOrder):
        self.start = template.Variable(start)
        self.total = template.Variable(total)
        self.openTab = template.Variable(openTab)
        self.query = template.Variable(query)
        self.indices = template.Variable(indices)
        self.sortField = template.Variable(sortField)
        self.sortOrder = template.Variable(sortOrder)

    def render(self, context):
        result = '<div class="pagination pagination-centered">\
                    <ul>'

        start = int(self.start.resolve(context))
        total = int(self.total.resolve(context))
        page = (start/settings.PAGE_SIZE) + 1
        onclick = """onclick="replaceContents('<img class=&quot;loader&quot; src=&quot;""" + settings.STATIC_URL + """img/ajax-loader.gif&quot;>');Dajaxice.Brownian.view.getData(replaceContents, {'type': '%s', 'query': '%s', 'indices': '%s', """ % (self.openTab.resolve(context), self.query.resolve(context), self.indices.resolve(context)) + """'sort': {&quot;%s&quot;: {&quot;order&quot;: &quot;%s&quot;}}, """ % (self.sortField.resolve(context), self.sortOrder.resolve(context)) + """'start': '%s'});" """
        if page == 1 and total > settings.PAGE_SIZE:
            result += '<li class="disabled"><a href="#">&laquo;</a></li>'
            result += '<li class="disabled"><a href="#">&lsaquo;</a></li>'
        elif total > settings.PAGE_SIZE:
            result += '<li><a href="#"' + onclick % 0 + '>&laquo;</a></li>'
            result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*(page-2)) + '>&lsaquo;</a></li>'
            result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*(page-2)) + '>' + str(page - 1) + '</a></li>'

        if total > settings.PAGE_SIZE:
            result += '<li class="active"><a href="#">' + str(page) + '</a></li>'

        if (start + settings.PAGE_SIZE) < total:
            result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*page) + '>' + str(page + 1) + '</a></li>'
            if (start + 2*settings.PAGE_SIZE) < total:
                result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*(page+1)) + '>' + str(page + 2) + '</a></li>'
                if (start + 3*settings.PAGE_SIZE) < total:
                        result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*(page+2)) + '>' + str(page + 3) + '</a></li>'

        if (start + settings.PAGE_SIZE) < total:
            result += '<li><a href="#"' + onclick % (settings.PAGE_SIZE*page) + '>&rsaquo;</a></li>'

        result += '</ul>\
                  </div>'

        return result

register.tag('paginate', genPagination)