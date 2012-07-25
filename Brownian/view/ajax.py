from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
import utils.es
import requests
import ast

@dajaxice_register
def getData(request, type, query, indices, sort, start=0):
    data = {}
    sort = ast.literal_eval(sort)
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
    data['total'] = result['hits']['total']
    try:
        if result['es_shards']['failed']:
            data['error'] = "%d of %d shards had failures." % (result['es_shards']['failed'], result['es_shards']['total'])
    except:
        pass
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