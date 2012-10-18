from django.shortcuts import render
import utils.es
from django.conf import settings

def query(request):
    """ This page is the main query interface.
    """
    data = {}

    params = request.GET

    # If we have a blank query, just return everything.
    query = params.get("query", "")
    if query == "": query = "*"
    data["query"] = query

    # If we have a blank time window, just return the past 15 minutes.
    time = params.get("time", "")
    if time == "": time = settings.DEFAULT_TIME_RANGE
    data["time"] = time
    if request.session.get('indices', False):
        indices = request.session.get('indices')
    else:
        try:
            indices = utils.es.getIndices()
        except:
            data["error"] = "Could not connect to server - please check ELASTICSEARCH_SERVER in settings.py"
            indices = []
            return render(request, "home.html", data)
        request.session['indices'] = indices

    data["health"]= utils.es.getHealth()
    result = utils.es.indicesFromTime(time, indices)
    selectedIndices = ",".join(result)
    data["indices"] = selectedIndices
    data["query"] = query
    data["start"] = 0
    data["root"] = request.path

    if not selectedIndices:
        data["error"] = "No indices found in that time range - please adjust your time range."
        return render(request, "home.html", data)

    try:
        data["hits"] = utils.es.getCounts(utils.es.queryEscape(query), index=selectedIndices)
    except:
        data["error"] = "Could not connect to ElasticSearch server for query - please check ElasticSearch cluster health."
        return render(request, "home.html", data)
    if not data["hits"]:
        data["error"] = "Query returned no hits."
        return render(request, "home.html", data)
    # To make the Javascript easier, we strip off the # from the currently open tab.
    # If we don't have an open tab, default to conn.
    openTab = params.get("openTab", "#conn").replace("#", "")

    if openTab in [result["type"] for result in data["hits"]]: data["openTab"] = openTab
    else:
        if data["hits"]: data["openTab"] = data["hits"][0]["type"]
        else: data["openTab"] = "conn"

    return render(request, "home.html", data)

def alerts(request):

    data = {}

    params = request.GET

    # If we have a blank time window, just return the past 15 minutes.
    time = params.get("time", "")
    if time == "": time = settings.DEFAULT_TIME_RANGE
    data["time"] = time
    if request.session.get('indices', False):
        indices = request.session.get('indices')
    else:
        try:
            indices = utils.es.getIndices()
        except:
            data["error"] = "Could not connect to server - please check ELASTICSEARCH_SERVER in settings.py"
            indices = []
            return render(request, "alerts.html", data)
        request.session['indices'] = indices

    data['health'] = utils.es.getHealth()
    result = utils.es.indicesFromTime(time, indices)
    selectedIndices = ",".join(result)
    data["indices"] = selectedIndices
    data["query"] = query
    data["start"] = 0
    data["root"] = request.path

    if not selectedIndices:
        data["error"] = "No indices found in that time range - please adjust your time range."
        return render(request, "alerts.html", data)
    facets = {"ips": {"terms": {"field": ["src", "dst"], "size": 25}},
              "ports": {"terms": {"field": "p", "size": 25}},
              "notices": {"terms": {"field": "note", "size": 25}},
              }
    data['facets'] = utils.es.doQuery("*", index=selectedIndices, size=0, type="notice", facets=facets)['facets']

    return render(request, "alerts.html", data)

def health(request):
    data = {}

    try:
        data['health'] = utils.es.getHealth()
        data['shards'] = utils.es.getShardInfo()
        data['nodes'] = utils.es.getNodeInfo()
    except:
        data["error"] = "Could not connect to server - please check ELASTICSEARCH_SERVER in settings.py"
        return render(request, "health.html", data)

    return render(request, "health.html", data)