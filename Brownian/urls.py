from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

dajaxice_autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'Brownian.view.views.query', name='query'),
    url(r'^notices/$', 'Brownian.view.views.alerts', name='alerts'),
    url(r'^health/$', 'Brownian.view.views.health', name='health'),
)

urlpatterns += staticfiles_urlpatterns()