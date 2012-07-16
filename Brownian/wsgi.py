import site

# Change this to where you installed Brownian
site.addsitedir('/opt/Brownian/lib/python2.7/site-packages/Brownian/wsgi.py')

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Brownian.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
