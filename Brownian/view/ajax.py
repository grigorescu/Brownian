from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
import utils.es

@dajaxice_register
def getData(request, type, query, indices):
    data = {}
    result = utils.es.doQuery(utils.es.queryEscape(query), index=indices, type=type)
    data['table'] = utils.es.resultToTable(result, type)
    return render_to_string("include/table.html", data)

