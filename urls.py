from django.conf.urls import patterns, include, url

urlpatterns = patterns('gallery.views',
    url(r'^$',                  'index'),
    url(r'^imagemap.xml$',      'imagemap'),
    url(r'^image/(?P<id>.+)/$', 'image'),
    url(r'^tag/(?P<tag>.+)/$',  'by_tag'),
    url(r'^(?P<id>([0-9]|[1-5][0-9]|6[0-3]))$', 'image_old_redirect'),
)
