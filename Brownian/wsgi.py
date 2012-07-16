BROWNIAN_PATH = '/opt/Brownian'
PYTHON_VER = '2.7'

import sys

sys.path.insert(0, BROWNIAN_PATH + '/lib/python' + PYTHON_VER + '/site-packages')

import site, os

site.addsitedir(BROWNIAN_PATH + '/lib/python' + PYTHON_VER + '/site-packages/Brownian/wsgi.py')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Brownian.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
