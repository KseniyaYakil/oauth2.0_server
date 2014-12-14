from django.conf.urls import patterns, url
from user_get_started import views

urlpatterns = patterns('',
		url(r'^$', views.home, name='home'),
		url(r'^registration/',  views.registration, name='registration'),
		url(r'^logout_user/', views.logout_user, name='logout_user'),
)
