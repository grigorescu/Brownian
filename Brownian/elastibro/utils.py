import json

import request
import errors

def getHealth(error_list=[]):
    """Get ElasticSearch cluster health"""
    health = {}
    responses, errored_clusters = request.get('_cluster/health')
    worst_status = "green"
    for cluster in responses.keys():
        try:
            health[cluster] = json.loads(responses[cluster].text)
        except ValueError:
            worst_status = "red"
            error_list.append(errors.errors['could_not_parse'] % cluster)
        try:
            status = health[cluster]['status']
            if worst_status != "red" and status != "green":
                worst_status = status
        except KeyError:
            worst_status = "red"
            error_list.append(errors.errors['could_not_get_health_status'] % cluster)

    health['_status'] = worst_status

    for cluster in errored_clusters.keys():
        error_list.append(errors.errors[errored_clusters[cluster]] % cluster)

    return (health, error_list)