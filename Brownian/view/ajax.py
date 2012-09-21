from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
import utils.es
import requests
import ast
import utils.plugins

@dajaxice_register
def getData(request, type, query, indices, sort, start=0):
    data = {}

    try:
        sort = ast.literal_eval(str(sort))
    except ValueError:
        raise ValueError(sort)

    try:
        result = utils.es.doQuery(utils.es.queryEscape(query), index=indices, type=type, start=start, sort=sort)
    except requests.ConnectionError:
        return "Error - Could not connect to ElasticSearch server for AJAX query."
    data['took'] = result['took']
    sortField, sortOrder = sort.items()[0]
    sortOrder = sortOrder['order']
    data['sort'] = {"field": sortField, "order": sortOrder}
    data['start'] = start
    data['openTab'] = type
    data['query'] = query.replace('"', "&quot;")
    data['indices'] = indices
    data['plugin_mapping'] = utils.plugins.mapping
    data['total'] = result['hits']['total']
    data['table'] = utils.es.resultToTable(result, type)
    return render_to_string("include/table.html", data)

@dajaxice_register
def updateIndices(request):
    try:
        indices = utils.es.getIndices()
    except requests.ConnectionError:
        raise requests.ConnectionError("Error - could not connect to ElasticSearch server to fetch indices.")
    request.session['indices'] = indices
    return True

@dajaxice_register
def runPlugin(request, displayName, args):
    for plugins in utils.plugins.mapping.values():
        for plugin in plugins:
            if plugin["displayName"] == displayName:
                return "<strong>" + displayName + ":</strong> " + plugin["plugin"].run([args])
    return "<strong>Error</strong>: Plugin not found."