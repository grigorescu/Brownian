import json

import request
import errors


def _loadResults(responses, errored_clusters, error_list=[], worst_status="green"):
    """Helper function to load the results and set a few error variables."""
    results = {}
    for cluster in responses.keys():
        if cluster in errored_clusters.keys():
            worst_status = "red"
            continue
        try:
            results[cluster] = json.loads(responses[cluster].text)
        except (ValueError, AttributeError):
            worst_status = "red"
            error_list.append(errors.errors['could_not_parse'] % cluster)

        results['_status'] = worst_status

    for cluster in errored_clusters.keys():
        error_list.append(errors.errors[errored_clusters[cluster]] % cluster)

    return (results, error_list)


## Health stuff


def getHealth(error_list=[]):
    """Get ElasticSearch cluster health"""
    responses, errored_clusters = request.get('_cluster/health')
    health, error_list = _loadResults(responses, errored_clusters, error_list=error_list)

    for cluster in health.keys():
        if cluster == "_status": continue
        try:
            status = health[cluster]['status']
            if health['_status'] != "red" and status != "green":
                health['_status'] = status
        except KeyError:
            health['_status'] = "red"
            error_list.append(errors.errors['could_not_get_health_status'] % cluster)

    return (health, error_list)


def getNodeInfo(error_list=[]):
    """Get ElasticSearch cluster node details"""
    responses, errored_clusters = request.get('_nodes/stats?clear=true&os=true&fs=true')
    nodes, error_list = _loadResults(responses, errored_clusters, error_list=error_list)

    for cluster in nodes.keys():
        if cluster == "_status": continue
        try:
            for node in nodes[cluster]['nodes'].keys():
                uptime = nodes[cluster]['nodes'][node]['os']['uptime']
        except KeyError:
            nodes['_status'] = "red"
            error_list.append(errors.errors['could_not_get_node_info'] % cluster)

    return nodes, error_list


def getShardInfo(error_list=[]):
    """Get ElasticSearch index shard details"""
    responses, errored_clusters = request.get('_stats?clear=true')
    shards, error_list = _loadResults(responses, errored_clusters, error_list=error_list)

    for cluster in shards.keys():
        if cluster == "_status": continue
        try:
            failed = shards[cluster]['_shards']['failed']
        except KeyError:
            shards['_status'] = "red"
            error_list.append(errors.errors['could_not_get_shard_info'] % cluster)

    return shards, error_list
