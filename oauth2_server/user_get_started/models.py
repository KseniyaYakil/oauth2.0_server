from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
		mobile_phone = models.CharField(max_length=15)
		birth_day = models.CharField(max_length=32)
