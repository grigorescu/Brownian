import requests, json
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

def queryFromString(query):
    """Execute a query across all types from a given query string.
    """
    queryString = ""
    # TODO - this is ugly - needs to be replaced with a count search type, with faceting per type.
    for i in types:
        queryString += '{"index": "%s", "type": "%s"}\n' % (settings.ELASTICSEARCH_INDEX, i)
        queryString += '{"query": {"query_string": {"query": "%s"}}, "size": %d}\n' % (query, settings.PAGE_SIZE)
    result = Request().msearch_scan(queryString)

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
        self.result = json.loads(result.replace('"_', '"es_'))
        if "error" in self.result.keys():
            raise IOError(self.result["error"])

        return self.result

    queryAll = lambda self: self._doRequest({"size": settings.PAGE_SIZE})
    query = lambda self, query: self._doRequest({"query": query, "size": settings.PAGE_SIZE})
    scan = lambda self, query: self._doRequest({"query": query}, search_opts="search_type=scan&scroll=10m&size=%d" % settings.PAGE_SIZE)
    msearch_scan = lambda self, data: self._doBulkRequest(data, operation="_msearch")
    facetsOnly = lambda self, facetQuery: self._doRequest({"facets": facetQuery, "size": 0})

