import requests
import Brownian.config

def get(path):
    """Issues a GET query against the ES servers, with the specified path."""

    responses = {}
    errored_clusters = {}

    for cluster in Brownian.config.elasticsearch_urls.keys():
        for i in range(len(Brownian.config.elasticsearch_urls[cluster])):
            es_url = Brownian.config.elasticsearch_urls[cluster][i]
            is_last = i == len(Brownian.config.elasticsearch_urls[cluster]) - 1
            try:
                r = requests.get(es_url + '/' + path.lstrip('/'))
            except requests.exceptions.ConnectionError:
                if is_last:
                    r = None
                    errored_clusters[cluster] = 'connection_error'
                else:
                    continue
            responses[cluster] = r
            break
    return responses, errored_clusters
