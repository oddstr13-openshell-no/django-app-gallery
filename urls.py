from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$',                  views.index),
    re_path(r'^imagemap.xml$',      views.imagemap),
    re_path(r'^image/(?P<id>.+)/$', views.image, name='gallery-image'),
    re_path(r'^tag/(?P<tag>.+)/$',  views.by_tag, name='gallery-by-tag'),
    re_path(r'^(?P<id>([0-9]|[1-5][0-9]|6[0-3]))$', views.image_old_redirect),
]
