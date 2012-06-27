import requests, json, datetime, string, pytz
import sys
from django.conf import settings
from broLogTypes import broLogs

types = [type for type, fields in broLogs]

def getIndices():
    """Get a list of all bro indexes
    """
    result = Request(index=None)._doRequest(operation="_stats", search_opts="clear=true&docs=true", verb="GET")
    indices = []
    for index_name, index_stats in result["es_all"]["indices"].items():
        if index_name.startswith(settings.ELASTICSEARCH_INDEX_PREFIX):
            index_name = str(index_name.replace("bro_", ""))
            indices.append({"time": index_name, "count": index_stats["total"]["docs"]["count"]})
    return indices

def indexNameToDatetime(indexName):
    """Convert a bro-201208121900 style-name to a datetime object.
    """
    indexTime = datetime.datetime.strptime(indexName.replace(settings.ELASTICSEARCH_INDEX_PREFIX, ""), "%Y%m%d%H%M")
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

    indices = [index["time"] for index in getIndices()]
    indices.sort()
    chosenIndices = []
    import sys
    for i in range(len(indices)):
        indexStart = indexNameToDatetime(indices[i])
        if indexStart >= then:
            print >>sys.stderr, "I believe that " + indexStart.strftime('%a %b %d %H:%M:%S.%f') + " is >= " + then.strftime('%a %b %d %H:%M:%S.%f')
            chosenIndices.append(indices[i])

        # What if our start is between two indices?
        if i < len(indices) - 1:
            if indexStart < then and indexNameToDatetime(indices[i+1]) > then:
                chosenIndices.append(indices[i])

    return ",".join(chosenIndices)

def queryEscape(query):
    """Certain chars need to be escaped
    """
    bad_chars = [("\\", "\\\\"),
        ("\"", "\\\""),
        ("[", "\u005b"),
        ("]", "\u005d"),
    ]
    for char, replacement in bad_chars:
        query = query.replace(char, replacement)

    return query

def queryFromString(query, index="_all"):
    """Execute a query across all types from a given query string.
    """
    queryString = ""
    # TODO - this is ugly - needs to be replaced with a count search type, with faceting per type.
    for i in types:
        queryString += '{"index": "%s", "type": "%s"}\n' % (index, i)
        queryString += '{"query": {"query_string": {"query": "%s"}}, "size": %d}\n' % (query, settings.PAGE_SIZE)
    result = Request(index=index).msearch_scan(queryString)

    return result

def resultToTabbedTables(result):
    """Convert an msearch result to a list of tables, sorted by type.
    """
    hits = []

    for i in range(len(result["responses"])):
        resultType = types[i]
        resultAnswer = result["responses"][i]
        header = [(field.name, field.type, field.description) for field in broLogs[i][1] if field.name not in settings.ELASTICSEARCH_IGNORE_COLUMNS.get(resultType, [])]
        content = []

        if resultType in settings.ELASTICSEARCH_IGNORE_TYPES:
            continue
        if "hits" not in resultAnswer.keys():
            continue
        if "hits" not in resultAnswer["hits"].keys():
            continue
        if len(resultAnswer["hits"]["hits"]) == 0:
            continue

        for hit in resultAnswer["hits"]["hits"]:
            row = []
            for column, fType, desc in header:
                row.append((column, fType, hit["es_source"].get(column, "")))
            content.append(row)

            if len(hit["es_source"].keys()) > len(row):
                assert "WARNING: Some fields weren't properly accounted for."
                assert "Type: %s;\nKnown fields: %s.\nRecvd fields: %s." % (resultType, hit["es_source"].keys(), [x[0] for x in row])

        hits.append({"header": header, "content": content, "type": resultType, "took": result["responses"][i]["took"],
                     "total": result["responses"][i]["hits"]["total"]})

    return hits



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
            result = requests.post(self.path + operation + "?" + search_opts, data=json.dumps(self.data)).text
        else:
            result = requests.get(self.path + operation + "?" + search_opts).text

        # ElasticSearch internal fields are prefixed with _. This causes some issues w/ Django, so we prefix with es_ instead.
        self.result = json.loads(result.replace('"_', '"es_'))
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    # TODO: Replace _doBulkRequest with a regular query, but with a search type of count with per-type faceting.
    def _doBulkRequest(self, data=None, operation="_search", search_opts=""):
        result = requests.post(self.path + operation + "?" + search_opts, data=data).text
        try:
            self.result = json.loads(result.replace('"_', '"es_'))
        except ValueError, e:
            print >>sys.stderr, result
            raise ValueError(e)
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    queryAll = lambda self: self._doRequest({"size": settings.PAGE_SIZE})
    query = lambda self, query: self._doRequest({"query": query, "size": settings.PAGE_SIZE})
    scan = lambda self, query: self._doRequest({"query": query}, search_opts="search_type=scan&scroll=10m&size=%d" % settings.PAGE_SIZE)
    msearch_scan = lambda self, data: self._doBulkRequest(data, operation="_msearch")
    facetsOnly = lambda self, facetQuery: self._doRequest({"facets": facetQuery, "size": 0})

