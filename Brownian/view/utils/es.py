import requests, json, datetime, string, pytz
from django.conf import settings
from broLogTypes import broLogs
import logging

logger = logging.getLogger('elasticsearch_requests')
def getIndices():
    """Get a list of all bro indexes
    """
    result = Request(index=None)._doRequest(operation="_stats", search_opts="clear=true", verb="GET")
    indices = []
    for index_name, index_stats in result["es_all"]["indices"].items():
        if index_name.startswith(settings.ELASTICSEARCH_INDEX_PREFIX):
            indices.append(index_name)
    return indices

def indexNameToDatetime(indexName):
    """Convert a bro-201208121900 style-name to a datetime object.
    """
    if indexName.startswith(settings.ELASTICSEARCH_INDEX_PREFIX) and not indexName.startswith(settings.ELASTICSEARCH_INDEX_PREFIX + "-"):
        return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now())

    indexTime = datetime.datetime.strptime(indexName.replace(settings.ELASTICSEARCH_INDEX_PREFIX + "-", ""), "%Y%m%d%H%M")
    return pytz.utc.localize(indexTime)

def indicesFromTime(startTime):
    """Create a comma-separated list of the indices one needs to query for the given time window.
    """
    endTime=pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now())
    number = ""
    unit = ""
    for i in range(len(startTime)):
        if startTime[i] in string.ascii_letters:
            unit = startTime[i:]
            try:
                number = int(number)
            except:
                raise ValueError("Format of time: 1m, 2days, etc.")
            break
        elif startTime[i] in string.whitespace:
            continue
        elif startTime[i] in string.digits:
            number += startTime[i]
        else:
            raise ValueError("Format of time: 1m, 2days, etc.")

    if not number or not unit or number < 1:
        raise ValueError("Format of time: 1m, 2days, etc.")

    units = {"day": ["day", "days", "d"],
             "hour": ["hour", "hours", "h"],
             "minute": ["minute", "minutes", "m"],
             "second": ["second", "seconds", "s"]}

    if unit in units["day"]:
        then = endTime - datetime.timedelta(days=number)
    elif unit in units["hour"]:
        then = endTime - datetime.timedelta(hours=number)
    elif unit in units["minute"]:
        then = endTime - datetime.timedelta(minutes=number)
    elif unit in units["second"]:
        then = endTime - datetime.timedelta(seconds=number)
    else:
        raise ValueError("Possible time units: " + units.keys())

    indices = getIndices()

    indices.sort()
    chosenIndices = []
    for i in range(len(indices)):
        indexStart = indexNameToDatetime(indices[i])

        if indexStart >= then:
            chosenIndices.append(indices[i])

        # What if our start is between two indices?
        if i < len(indices) - 1:
            if indexStart < then and indexNameToDatetime(indices[i+1]) > then:
                chosenIndices.append(indices[i])

    # Finally, if we have no indices, we include the last one, as we don't know when it ended
    if len(chosenIndices) == 0:
        chosenIndices.append(indices[-1])
    elif len(chosenIndices) == 1 and chosenIndices[0] == settings.ELASTICSEARCH_INDEX_PREFIX:
        chosenIndices.append(indices[-1])

    return chosenIndices

def queryEscape(query):
    """Certain chars need to be escaped
    """
    bad_chars = [("\\", "\\\\"),
        ("\"", "\\\""),
        ("::", "\\:\\:")
    ]
    for char, replacement in bad_chars:
        query = query.replace(char, replacement)

    return query

def getCounts(query, index="_all", type=None):
    """Using a facet of types, return dict of type and count.
    """
    hits = []

    data = {"query":
            {"constant_score":
             {"filter":
              {"query":
               {"query_string": {"query": query}}}}},
             "facets": {"term": {"terms": {"field": "_type", "size": 50, "order": "term"}}},
             "size": 0
            }
    result = Request(index=index, type=type)._doRequest(data=data)

    for i in result["facets"]["term"]["terms"]:
        count, type = i.itervalues()
        if type not in settings.ELASTICSEARCH_IGNORE_TYPES:
            hits.append({"type": type, "total": count})

    return hits

def doQuery(query, index="_all", type=None, start=0):
    """Short wrapper for simple queries.
    """
    data = {"query":
            {"constant_score":
             {"filter":
              {"query":
               {"query_string": {"query": query}}}}},
            "size": settings.PAGE_SIZE,
            "from": start,
            "sort": "ts",
            }
    result = Request(index=index, type=type)._doRequest(data=data)
    return result

def resultToTable(result, type):
    """Convert JSON result to a dict for use in HTML table template.
    """
    logger.debug(result)
    header = [(field.name, field.type, field.description) for field in broLogs[type] if field.name not in settings.ELASTICSEARCH_IGNORE_COLUMNS.get(type, [])]
    content = []

    if type in settings.ELASTICSEARCH_IGNORE_TYPES:
        return {}
    if "hits" not in result.keys():
        return {}
    if "hits" not in result["hits"].keys():
        return {}
    if len(result["hits"]["hits"]) == 0:
        return {}

    for hit in result["hits"]["hits"]:
        row = []
        for column, fType, desc in header:
            row.append((column, fType, hit["es_source"].get(column, "")))
        content.append(row)

        if len(hit["es_source"].keys()) > len(row):
            assert "WARNING: Some fields weren't properly accounted for."
            assert "Type: %s;\nKnown fields: %s.\nRecvd fields: %s." % (type, hit["es_source"].keys(), [x[0] for x in row])

    return {"header": header, "content": content, "took": result["took"]}

class Request(object):
    """A single request to ElasticSearch
    """
    def __init__(self, index="_all", type=None, url=settings.ELASTICSEARCH_SERVER):
        path = "http://%s/" % url
        if index:
            path += index + "/"
            if type:
                path += type + "/"
        self.path = path
        self.data = {}

    def _doRequest(self, data=None, operation="_search", search_opts="", verb="POST"):
        if data:
            self.data = dict(self.data.items() + data.items())

        if verb == "POST":
            logger.debug("POST " + self.path + operation + "?" + search_opts)
            logger.debug("      " + json.dumps(self.data))
            result = requests.post(self.path + operation + "?" + search_opts, data=json.dumps(self.data)).text
        else:
            logger.debug("GET " + self.path + operation + "?" + search_opts)
            result = requests.get(self.path + operation + "?" + search_opts).text

        # ElasticSearch internal fields are prefixed with _. This causes some issues w/ Django, so we prefix with es_ instead.
        self.result = json.loads(result.replace('"_', '"es_'))
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    # TODO: Replace _doBulkRequest with a regular query, but with a search type of count with per-type faceting.
    def _doBulkRequest(self, data=None, operation="_search", search_opts=""):
        result = requests.post(self.path + operation + "?" + search_opts, data=data).text
        logger.debug("BULK " + self.path + operation + "?" + search_opts)
        logger.debug("      " + data)
        self.result = json.loads(result.replace('"_', '"es_'))
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    queryAll = lambda self: self._doRequest({"size": settings.PAGE_SIZE})
    query = lambda self, query: self._doRequest({"query": query, "size": settings.PAGE_SIZE})
    scan = lambda self, query: self._doRequest({"query": query}, search_opts="search_type=scan&scroll=10m&size=%d" % settings.PAGE_SIZE)
    msearch_scan = lambda self, data: self._doBulkRequest(data, operation="_msearch")
    facetsOnly = lambda self, facetQuery: self._doRequest({"facets": facetQuery, "size": 0})

