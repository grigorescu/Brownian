from django.conf.urls import patterns, url

urlpatterns = patterns('Brownian.view.views',
    url(r'^$', 'home'),
    url(r'^query/*', 'query'),
)
