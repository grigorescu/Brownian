from django.shortcuts import render
from django.conf import settings
import utils.es
from utils.broLogTypes import broLogs
import sys

def home(request):
    """ This page is just a simple landing page."""

    data = {}
    return render(request, "home.html", data)

def query(request):
    """ This page is the main query interface."""

    data = {}
    params = request.GET

    # If we have a blank query, just return everything.
    query = params.get("query", "*")
    if query == "": query = "*"

    # To make the Javascript easier, we strip off the # from the currently open tab.
    # If we don't have an open tab, default to conn.
    openTab = params.get("openTab", "#conn").replace("#", "")

    data["query"] = query
    # Certain chars need to be escaped
    for char in ["\\", "+", "-", "&&", "||", "(", ")", "{", "}", "^", "\""]:
        query = query.replace(char, "".join(["\\" + x for x in char]))

    types = [type for type, fields in broLogs]
    queryString = ""

    # TODO - this is ugly - needs to be replaced with a count search type, with faceting per type.
    for i in types:
        queryString += '{"index": "bro_062220", "type": "%s"}\n' % i
        queryString += '{"query": {"query_string": {"query": "%s"}}, "size": 25}\n' % query
    result = utils.es.Request().msearch_scan(queryString)

    data["hits"] = []

    for i in range(len(result["responses"])):
        resultType = types[i]
        resultAnswer = result["responses"][i]
        header = [(field.name, field.description) for field in broLogs[i][1] if field.name not in settings.ELASTICSEARCH_IGNORE_COLUMNS.get(resultType, [])]
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
            for column, desc in header:
                row.append((column, hit["es_source"].get(column, "")))
            content.append(row)
            if len(hit["es_source"].keys()) > len(row):
                print >>sys.stderr, "WARNING: Some fields weren't properly accounted for."
                print >>sys.stderr, "Type: %s; Fields: %s." % (resultType, hit["es_source"].keys())
        data["hits"].append({"header": header, "content": content, "type": resultType,
                            "took": result["responses"][i]["took"],
                            "total": result["responses"][i]["hits"]["total"]})

    if openTab in [result["type"] for result in data["hits"]]:
        data["openTab"] = openTab
    else:
        if data["hits"]:
            data["openTab"] = data["hits"][0]["type"]
        else:
            # If we have no hits, this is really not an issue, since we won't loop through anything. Just to be sure:
            data["openTab"] = "conn"

    return render(request, "query.html", data)
