from django import forms
from django.forms import PasswordInput, ValidationError
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import User

class RegForm(forms.Form):
		username = forms.CharField(label='User name', max_length=64)
		password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())
		name = forms.CharField(label='Real name', max_length=128)
		email = forms.EmailField(label='Email')
		mobile_phone = forms.CharField(label='Mobile phone', max_length=15)
		birth_day = forms.CharField(label='Birthday', max_length=32)

		def clean(self):
				super(RegForm, self).clean()

				data = self.cleaned_data
				try:
					User.objects.create_user(username=data['username'], email=data['email'], password=data['password'],
												first_name=data['name'], mobile_phone=data['mobile_phone'], birth_day=data['birth_day'])
				except IntegrityError as e:
						raise ValidationError('Specified user exists')
				self.user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
