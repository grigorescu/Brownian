# TODO: Move this to a better place.

import requests, json
from django.conf import settings

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

    def _doRequest(self, data=None, operation="_search", search_opts=""):
        if data:
            self.data = dict(self.data.items() + data.items())

        result = requests.post(self.path + operation + "?" + search_opts, data=json.dumps(self.data)).text

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

    # TODO: While these are handy, sizes need to be customizable.
    queryAll = lambda self: self._doRequest({"size": 50})
    query = lambda self, query: self._doRequest({"query": query, "size": 500})
    scan = lambda self, query: self._doRequest({"query": query}, search_opts="search_type=scan&scroll=10m&size=25")
    msearch_scan = lambda self, data: self._doBulkRequest(data, operation="_msearch")
    facetsOnly = lambda self, facetQuery: self._doRequest({"facets": facetQuery, "size": 0})

