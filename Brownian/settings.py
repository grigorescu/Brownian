# Common Application Settings

# How many results per page.
PAGE_SIZE=30

# When running in an actual web server, edit this to the directory Brownian is being installed in.
# e.g. https://server/Brownian -> DAJAXICE_MEDIA_PREFIX="Brownian/dajaxice"
DAJAXICE_MEDIA_PREFIX="dajaxice"

# ElasticSearch settings

# Hostname and port of your ElasticSearch server
ELASTICSEARCH_SERVER = "localhost:9200"

# Index name prefix
ELASTICSEARCH_INDEX_PREFIX = "bro"

# Don't ever show results for these types.
ELASTICSEARCH_IGNORE_TYPES = [
    "communication",
    "loaded_scripts",
    "notice_alarm",
    "notice_policy",
    ]

# Hide these columns for these types.
ELASTICSEARCH_IGNORE_COLUMNS = {
    "conn": ["missed_bytes", ],
    "ftp": ["mime_desc", ],
    "notice": ["actions", "dropped", "peer_descr", "policy_items", "suppress_for", ],
    "notice_alarm": ["actions", "dropped", "peer_descr", "policy_items", "suppress_for", ],
    "smtp_entities": ["excerpt", ],
    "weird": ["peer"],
}

# Date/Time stuff

TIME_ZONE = 'US/Eastern'

# Django settings for Brownian project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ( # ('Your Name', 'your_email@example.com'),
 )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'Brownian_temp_data'
        },
    }

SESSION_COOKIE_AGE = 300

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False # This isn't used.
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ( )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '62a=4)pj*u&amp;*aj*1d4f+!tpq5uf@!82t2cx(pu7)_12=)afv6$'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Brownian.urls'
WSGI_APPLICATION = 'Brownian.wsgi.application'

INSTALLED_APPS = (
    'Brownian.view',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'dajaxice',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'elasticsearch_requests': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'dajaxice': {
            'handlers': ['console'],
            'level': 'ERROR',
            }
    }
}
