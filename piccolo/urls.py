__author__ = 'ads'

from django.conf.urls import patterns, include, url
from piccolo import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='root_path'),
                       url(r'^prerequisites/$', views.prerequisites),
                       url(r'^theyboughtthis/$', views.theyboughtthis),
                       url(r'^about/$', views.about),
                       url(r'^payload/$', views.payload),
                       url(r'^welcome/$', views.welcome)
                       )