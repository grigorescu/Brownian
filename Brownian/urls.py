from django.conf.urls import patterns, url, include
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(r'^$', 'Brownian.view.views.query'),
)
