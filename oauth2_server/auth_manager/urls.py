from django.conf.urls import patterns, url
from auth_manager import views

urlpatterns = patterns('',
	url(r'^$', views.auth_code_req, name='auth20'),
	url(r'^token', views.get_access_token, name='get_access_token'),
	#url(r'^conns/$', views.connections, name='user_connections'),
	#url(r'^conns/(?P<conn_id>\d+)/$', views.connect_info, name='user_conn_info'),
)
