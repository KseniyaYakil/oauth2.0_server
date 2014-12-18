from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^position/', views.position, name='position'),
		#url(r'^position/(?{<pos_id>\d+/$', views.position_id, name='position_id'),
)
