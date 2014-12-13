from django.db import models

# Create your models here.

class client_info(models.Model):
		client_id = models.CharField(max_length=1024)
		client_secret = models.CharField(max_length=1024)
		redirect_domain = models.URLField(max_length=1024)
		client_name = models.CharField(max_length=1024)

class access_token(models.Model):
		token = models.CharField(max_length=1024)
		creation_time = models.DateTimeField(auto_now=True)
		app_id = models.ForeignKey(client_info)
		refresh_token = models.CharField(max_length=1024)


