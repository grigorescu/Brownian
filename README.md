Brownian
================================

Brownian is a web interface for viewing and interacting with [Bro IDS](http://bro-ids.org/) logs.

Prerequisites
-------------

This interface only works with Bro if you're using the new [ElasticSearch Logging](http://git.bro-ids.org/bro.git/blob/refs/heads/topic/seth/elasticsearch:/doc/logging-elasticsearch.rst) plugin.

Please refer to that documentation for getting ElasticSearch setup, and receiving logs.

Requirements
------------

* Python 2, version 2.6 or greater.
* Brownian comes with it's own webserver, for testing purposes. For production use, you will want to configure Apache or a similar server. (TODO: Add instructions).

Virtualenv Setup
----------------

It is advised to run Brownian in a [virtualenv](http://www.virtualenv.org/en/latest/index.html) - an isolated Python environment with its own set of libraries.
This will prevent system upgrades from modifying the globally installed libraries and potentially breaking Brownian.

1. For installing virtualenv, please see: (http://www.virtualenv.org/en/latest/index.html#installation).
+ Once installed, create and switch to your environment:
```bash
$ virtualenv Brownian
$ cd Brownian
$ source ./bin/activate
```

Installation
------------

```bash
$ pip install git+https://github.com/grigorescu/Brownian.git
```

The files are installed in ./lib/python2.7/site-packages/Brownian.

Configuration
-------------

Change ELASTICSEARCH_SERVER in Brownian/settings.py to your server's hostname and port.

Running Development Server
--------------------------
```bash
$ export DJANGO_SETTINGS_MODULE=Brownian.settings
$ python ./Brownian/bin/django-admin.py runserver
```

TODO
----

Please see the issues section.
