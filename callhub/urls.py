from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^login/', include('shopify_app.urls')),
                       url(r'^', include("piccolo.urls"), name='root_path'),
                       )
