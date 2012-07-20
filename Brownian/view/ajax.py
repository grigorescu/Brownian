from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
import utils.es
import requests

@dajaxice_register
def getData(request, type, query, indices, start=0):
    data = {}
    try:
        result = utils.es.doQuery(utils.es.queryEscape(query), index=indices, type=type, start=start)
    except requests.ConnectionError:
        return "Error - Could not connect to ElasticSearch server for AJAX query."
    data['took'] = result['took']
    data['start'] = start
    data['openTab'] = type
    data['query'] = query.replace('"', "&quot;")
    data['indices'] = indices
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