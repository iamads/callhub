from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/', include('shopify_app.urls')),
                       url(r'^', include("piccolo.urls"), name='root_path'),
                       )
