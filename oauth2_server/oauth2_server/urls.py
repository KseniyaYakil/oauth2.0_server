from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'oauth2_server.views.home', name='home'),
    url(r'^auth/', include('auth_manager.urls')),
    url(r'^user/', include('user_get_started.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
