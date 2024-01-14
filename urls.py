from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                  views.index),
    url(r'^imagemap.xml$',      views.imagemap),
    url(r'^image/(?P<id>.+)/$', views.image, name='gallery-image'),
    url(r'^tag/(?P<tag>.+)/$',  views.by_tag, name='gallery-by-tag'),
    url(r'^(?P<id>([0-9]|[1-5][0-9]|6[0-3]))$', views.image_old_redirect),
]
