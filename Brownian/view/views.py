from django.shortcuts import render
import utils.es
import requests

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
    if time == "": time = "15m"
    data["time"] = time
    if request.session.get('indices', False):
        indices = request.session.get('indices')
    else:
        try:
            indices = utils.es.getIndices()
        except requests.ConnectionError:
            return "Error - could not connect to ElasticSearch server to fetch indices."
        request.session['indices'] = indices

    result = utils.es.indicesFromTime(time, indices)
    selectedIndices = ",".join(result)
    data["indices"] = selectedIndices
    data["query"] = query
    data["start"] = 0
    try:
        data["hits"] = utils.es.getCounts(utils.es.queryEscape(query), index=selectedIndices)
    except requests.ConnectionError:
        return "Error - could not connect to ElasticSearch server for query."

    # To make the Javascript easier, we strip off the # from the currently open tab.
    # If we don't have an open tab, default to conn.
    openTab = params.get("openTab", "#conn").replace("#", "")

    if openTab in [result["type"] for result in data["hits"]]: data["openTab"] = openTab
    else:
        if data["hits"]: data["openTab"] = data["hits"][0]["type"]
        else: data["openTab"] = "conn"

    return render(request, "home.html", data)
