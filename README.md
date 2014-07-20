Brownian [![Build Status](https://secure.travis-ci.org/grigorescu/Brownian.png?branch=master)](http://travis-ci.org/grigorescu/Brownian)
================================

Brownian is a web interface for viewing and interacting with [Bro IDS](http://bro.org/) logs. Try it out on a [live demo](http://brownian.bro.org/?time=all).

Why Brownian?
-------------

Brownian motion relates to the elastic collisions and random motion of particles. Brownian aims to help you leverage Bro and ElasticSearch to make sense of a massive amount of seemingly random data.

Prerequisites
-------------

This interface only works with Bro if you're using the new [ElasticSearch Logging](http://bro.org/sphinx/frameworks/logging-elasticsearch.html) plugin.

Please refer to that documentation for getting ElasticSearch setup, and receiving logs.

It's also *highly* recommended to review the [ElasticSearch configuration tips](https://github.com/grigorescu/Brownian/wiki/ElasticSearch-Configuration).

Requirements
------------

* Python version 2.6 or 2.7.
* Brownian comes with it's own webserver, for testing purposes.
* For production use, Apache with mod_wsgi is recommended.

Virtualenv Setup
----------------

It is advised to run Brownian in a [virtualenv](http://www.virtualenv.org/en/latest/index.html) - an isolated Python environment with its own set of libraries.
This will prevent system upgrades from modifying the globally installed libraries and potentially breaking Brownian.

1. Download the latest [virtualenv.py](https://raw.github.com/pypa/virtualenv/master/virtualenv.py).
+ Create and switch to your environment:

```bash
$ python ./virtualenv.py Brownian
$ cd Brownian
$ source ./bin/activate
```

Installation
------------

```bash
$ pip install git+https://github.com/grigorescu/Brownian.git
```

The files are installed in ./lib/python2.X/site-packages/Brownian.

Configuration
-------------

1. Change ```ELASTICSEARCH_SERVER``` in Brownian/lib/python2.X/site-packages/Brownian/settings.py to your server's hostname and port.
+ Change ```TIME_ZONE``` in settings.py to your desired timezone.
+ Review the other settings at the top of settings.py and configure them as desired.

Running the Development Server
------------------------------
```bash
$ export DJANGO_SETTINGS_MODULE=Brownian.settings
```
In settings.py, modify the ```DATABASES``` setting to the path you'd like a small SQLite database created (your user will need write permissions to both the file and the parent directory).
```bash
$ python ./bin/django-admin.py syncdb
$ python ./bin/django-admin.py runserver
```

Running the Production Server with Apache
-----------------------------------------
1. Install mod_wsgi
+ Edit ```BROWNIAN_PATH``` at the top of Brownian/lib/python2.X/site-packages/Brownian/wsgi.py to the location of your virtualenv directory.
+ In settings.py, modify the ```DATABASES``` setting to the path you'd like a small SQLite database created (your Apache user will need write permissions to both the file and the parent directory).
+ To create the database, in your virtualenv, run ```DJANGO_SETTINGS_MODULE=Brownian.settings ./bin/django-admin.py syncdb```. You don't need to create any users.
+ Edit your Apache config to include:

```conf
WSGIPassAuthorization on
WSGIScriptAlias "/Brownian" "/opt/Brownian/lib/python2.X/site-packages/Brownian/wsgi.py"

# Static content - CSS, Javascript, images, etc.
Alias /static/ /opt/Brownian/lib/python2.X/site-packages/Brownian/view/static/
<Directory /opt/Brownian/lib/python2.X/site-packages/Brownian/view/static>
  Order allow,deny
  Allow from all
</Directory>

# Optional - Permissions
<Directory /opt/Brownian/lib/python2.X/site-packages/Brownian>
Allow from ...
... Blah blah ...
</Directory>
```

Finally, restart Apache, and you should be good to go.

If you'd like to have your static files somewhere other than ```/static```, change ```STATIC_URL``` in settings.py. Please make sure to leave a trailing slash.

For more information, see: https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/

Issues
------

If you see something that's broken, or something that you'd like added, please create an issue.

As always, fork, patch, and push away!

