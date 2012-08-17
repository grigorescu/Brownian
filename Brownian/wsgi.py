BROWNIAN_PATH = '/opt/Brownian'

import sys
version = sys.version_info
PYTHON_VER = "%d.%d" % (version[0], version[1])

sys.path.insert(0, BROWNIAN_PATH + '/lib/python' + PYTHON_VER + '/site-packages')

import site, os

site.addsitedir(BROWNIAN_PATH + '/lib/python' + PYTHON_VER + '/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Brownian.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
