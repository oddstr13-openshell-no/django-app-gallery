from django.conf.urls import patterns, include, url

urlpatterns = patterns('gallery.views',
    url(r'^$',                  'index'),
    url(r'^image/(?P<id>.+)/$', 'image'),
    url(r'^tag/(?P<tag>.+)/$',  'by_tag'),
)
