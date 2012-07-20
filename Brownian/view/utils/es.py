import requests, json, datetime, string, pytz
from django.conf import settings
from broLogTypes import broLogs
import logging

logger = logging.getLogger('elasticsearch_requests')

def getIndices():
    """Get a list of all bro indices
    """
    result = Request(index="@bro-meta")._doRequest({"size": 65535})
    indices = []
    for hit in result["hits"]["hits"]:
        if hit["es_source"]["name"].startswith(settings.ELASTICSEARCH_INDEX_PREFIX):
            indices.append(hit["es_source"])

    return indices

def indexNameToDatetime(indexName):
    """Convert a bro-201208121900 style-name to a datetime object.
    """
    if indexName.startswith(settings.ELASTICSEARCH_INDEX_PREFIX) and not indexName.startswith(settings.ELASTICSEARCH_INDEX_PREFIX + "-"):
        return pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now())

    indexTime = datetime.datetime.strptime(indexName.replace(settings.ELASTICSEARCH_INDEX_PREFIX + "-", ""), "%Y%m%d%H%M")
    return pytz.timezone(settings.TIME_ZONE).localize(indexTime)

def indicesFromTime(startTime, indices):
    """Create a comma-separated list of the indices one needs to query for the given time window.
    """
    endTime=pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.now())

    if startTime == "all":
        return [index["name"] for index in indices]
    else:
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

    chosenIndices = []
    for index in indices:
        indexStart = pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.utcfromtimestamp(index["start"]))
        indexEnd = pytz.timezone(settings.TIME_ZONE).localize(datetime.datetime.utcfromtimestamp(index["end"]))

        if (indexStart >= then and indexEnd <= endTime) or (indexStart < then and indexStart < endTime and indexEnd >= then):
                chosenIndices.append(index["name"])

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
            "sort": {"ts": {"order": "desc"}},
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
        self.requests_config = {"max_retries": 0}

    def _doRequest(self, data=None, operation="_search", search_opts="", verb="POST"):
        if data:
            self.data = dict(self.data.items() + data.items())

        if verb == "POST":
            logger.debug("POST " + self.path + operation + "?" + search_opts)
            logger.debug("      " + json.dumps(self.data))
            result = requests.post(self.path + operation + "?" + search_opts, data=json.dumps(self.data), config=self.requests_config).text

        else:
            logger.debug("GET " + self.path + operation + "?" + search_opts)
            result = requests.get(self.path + operation + "?" + search_opts, config=self.requests_config).text

        # ElasticSearch internal fields are prefixed with _. This causes some issues w/ Django, so we prefix with es_ instead.
        self.result = json.loads(result.replace('"_', '"es_'))
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    queryAll = lambda self: self._doRequest({"size": settings.PAGE_SIZE})
    query = lambda self, query: self._doRequest({"query": query, "size": settings.PAGE_SIZE})

