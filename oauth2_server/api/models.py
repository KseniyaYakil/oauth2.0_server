from django.db import models
from user_get_started.models import User

class Position(models.Model):
		name = models.CharField(max_length=30)
		salary = models.IntegerField(default=5000)
		salary_currency = models.CharField(max_length=10, default='rub')

class Employe(models.Model):
		user = models.ForeignKey(User)
		position = models.ForeignKey(Position)
