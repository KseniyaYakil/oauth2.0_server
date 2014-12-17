from django.db import models
from .config import AuthConf

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

		def is_expired(self):
				return (datetime.now() - self.creation_time).total_seconds >= AuthConf.access_exp_time

class auth_code(models.Model):
		code = models.CharField(max_length=64)
		client_id = models.ForeignKey(client_info)
		creation_time = models.DateTimeField(auto_now=True)

		def is_expired(self):
				return (datetime.now() - self.creation_time).total_seconds >= AuthConf.auth_exp_time


