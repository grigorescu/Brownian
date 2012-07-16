Brownian [![Build Status](https://secure.travis-ci.org/grigorescu/Brownian.png)](http://travis-ci.org/grigorescu/Brownian)
================================

Brownian is a web interface for viewing and interacting with [Bro IDS](http://bro-ids.org/) logs. [Screenshots](http://imgur.com/a/vfhCf)!

Why Brownian?
-------------

Brownian motion relates to the elastic collisions and random motion of particles. Brownian aims to help you leverage Bro and ElasticSearch to make sense of a massive amount of seemingly random data.

Prerequisites
-------------

This interface only works with Bro if you're using the new [ElasticSearch Logging](http://git.bro-ids.org/bro.git/blob/refs/heads/topic/seth/elasticsearch:/doc/logging-elasticsearch.rst) plugin.

Please refer to that documentation for getting ElasticSearch setup, and receiving logs.

It's also *highly* recommended to review the [ElasticSearch configuration tips](https://github.com/grigorescu/Brownian/wiki/ElasticSearch-Configuration).

Requirements
------------

* Python 2, version 2.6 or greater.
* Brownian comes with it's own webserver, for testing purposes.
* For production use, [configure Apache with mod_wsgi](https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/), and point it to Brownian/wsgi.py.

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

1. Change ELASTICSEARCH_SERVER in Brownian/lib/python2.7/site-packages/Brownian/settings.py to your server's hostname and port.
+ Change TIME_ZONE in settings.py to your desired timezone.
+ Review the other settings at the top of settings.py and configure them as desired.

Running the Development Server
------------------------------
```bash
$ export DJANGO_SETTINGS_MODULE=Brownian.settings
$ python ./bin/django-admin.py runserver
```

Running the Production Server with Apache
-----------------------------------------
1. Install mod_wsgi
+ Edit BROWNIAN_PATH at the top of Brownian/lib/python2.7/site-packages/Brownian/wsgi.py to the location of your virtualenv directory.
+ If you're not using Python 2.7, edit PYTHON_VER at the top of wsgi.py.
+ Edit your Apache config to include:

```conf
WSGIPassAuthorization on
WSGIScriptAlias "/Brownian" "/opt/Brownian/lib/python2.7/site-packages/Brownian/wsgi.py"

# Static content - CSS, Javascript, images, etc.
Alias /static/ /opt/Brownian/lib/python2.7/site-packages/Brownian/view/static/
<Directory /opt/Brownian/lib/python2.7/site-packages/Brownian/view/static>
  Order allow,deny
  Allow from all
</Directory>

# Optional - Permissions
<Directory /opt/Brownian/lib/python2.7/site-packages/Brownian>
Allow from ...
... Blah blah ...
</Directory>
```

Finally, restart Apache, and you should be good to go.

Issues
------

If you see something that's broken, or something that you'd like added, please create an issue.

As always, fork, patch, and push away!

