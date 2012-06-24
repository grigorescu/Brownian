from django.shortcuts import render
import es

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

    # TODO - this is cool but ugly - needs to be replaced with a count search type, with faceting per type.
    result = es.Request().msearch_scan("""
            {"index": "bro_062220", "type": "conn"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "dns"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "smtp"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "software"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "notice_policy"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "ssl"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "notice_alarm"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "ssh"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "syslog"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "known_services"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "known_hosts"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "http"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "smtp_entities"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "irc"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "known_certs"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "ftp"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "notice"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "weird"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "dpd"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "tunnel"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "socks"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            {"index": "bro_062220", "type": "signatures"}
            {"query": {"query_string": {"query": """ + '"' + query + '"' + """}}, "size": 25}
            """)

    data["hits"] = {}
    types = ["conn", "dns", "smtp", "software", "notice_policy", "ssl", "notice_alarm", "ssh", "syslog", "known_services",
             "known_hosts", "http", "smtp_entities", "irc", "known_certs", "ftp", "notice", "weird", "dpd", "tunnel",
             "socks", "signatures"]

    # Have to to a bit of tweaking because not every result row will have all the fields.
    # TODO: Figure out a way to arrange the columns.
    for i in range(len(result["responses"])):
        header = []
        content = []
        for hit in result["responses"][i]["hits"]["hits"]:
            row = [""]*len(header)
            for key, value in hit["es_source"].items():
                if key not in header:
                    header.append(key)
                    row.append((key, value))
                else:
                    row[header.index(key)] = (key, value)
            content.append(row)
        if header:
            data["hits"][types[i]] = {"header": header, "content": content, "type": types[i],
                                      "took": result["responses"][i]["took"], "total": result["responses"][i]["hits"]["total"]}

    if openTab in data["hits"].keys():
        data["openTab"] = openTab
    else:
        if data["hits"]:
            data["openTab"] = data["hits"].keys()[0]
        else:
            # If we have no hits, this is really not an issue, since we won't loop through anything.
            data["openTab"] = "conn"

    return render(request, "query.html", data)
