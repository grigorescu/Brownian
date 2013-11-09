##################################################
#### config.py                                ####
####                                          ####
#### Configuration for site-specific settings ####
##################################################

## Step 1: Define your elasticsearch clusters
##
## Each cluster can have multiple nodes that Brownian will query, in order.
## Format: A list of strings, in the format http(s)://host:port. Host can be either an IP address or a hostname.

main_es_cluster = ['http://127.0.0.1:9200',
                   #'http://fallback.localdomain:9200',
                  ]
#remote_campus_es_cluster = ['http://es.blah.edu:9200']

## elasticsearch_urls
##
## Description: Now that we defined each cluster, this dictionary collects them all together and gives them a handy
##              name.
## Format: pretty_print_name: list of urls, as defined above.

elasticsearch_urls = {'main': main_es_cluster,
                      #'remote': remote_campus_es_cluster,
                     }
