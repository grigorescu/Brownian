from django.conf.urls import patterns, url, include
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    (r'^dajaxice/', include('dajaxice.urls')),
    url(r'^$', 'Brownian.view.views.query', name='query'),
)
