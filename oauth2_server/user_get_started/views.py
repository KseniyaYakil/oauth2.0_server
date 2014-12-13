from django.shortcuts import render, redirect
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from .user_forms import RegForm
from django.db import IntegrityError

@csrf_exempt
def registration(request):
		if request.method == 'GET':
				reg_form = RegForm()
				return render(request, 'user_get_started/registration.html', {'form' : reg_form})

		reg_form = RegForm(request.POST)
		if not reg_form.is_valid():
				return render(request, 'user_get_started/registration.html', {'form' : reg_form})

		user = reg_form.user
		if user is not None:
				login(request, reg_form.user)
		else:
				print("ERR: unabled to register user `{0}'").format(user['username'])
				raise Http404

		return HttpResponse("You have been succesfully loginned!")

def home(request):
		return render(request, 'user_get_started/home.html', {'user' : request.user})

def logout_user(request):
		logout(request)
		return redirect('user/')

