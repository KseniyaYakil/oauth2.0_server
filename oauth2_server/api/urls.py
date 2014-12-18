from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^me$', views.me, name='me'),
		url(r'^position$', views.position, name='position'),
		url(r'^employe$', views.employes, name='employes' ),
		url(r'^employe/(?P<emp_id>\d+)$', views.employe_id, name='employe_id' ),
		url(r'^position/(?P<pos_id>\d+)$', views.position_id, name='position_id' ),
)
