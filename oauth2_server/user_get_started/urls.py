from django.conf.urls import patterns, url
from user_get_started import views

urlpatterns = patterns('',
		url(r'^$', views.home, name='home'),
		url(r'^registration/',  views.registration, name='registration'),
		url(r'^logout/', views.logout_user, name='log_out'),
)
