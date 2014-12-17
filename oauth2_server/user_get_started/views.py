from django.shortcuts import render, redirect
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from .user_forms import RegForm, LoginForm
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

		#TODO:redirect to loggined user home page
		return HttpResponse("You have been succesfully registrated and loginned!")

def home(request):
		return render(request, 'user_get_started/home.html', {'user' : request.user})

def login_user(request):
		if request.method == 'GET':
				login_form = LoginForm()
				return render(request, 'user_get_started/login_user.html', {'form' : login_form})

		login_form = LoginForm(request.POST)
		if not login_form.is_valid():
				return render(request, 'user_get_started/login_user.html', {'form' : login_form})

		user = login_form.user
		if user is None:
				print "ERR: user doesn't exist or password is insorrect"
				return HttpResponse("Specified user doesn't exist or password is incorrect")

		login(request, user)

		if 'redirect_internal' in request.session:
				for key, value in request.session['get_params'].items():
						print "login: {0} -> {1}".format(key, value)
				return redirect(request.session['redirect_internal'])

		#TODO:redirect to loggined user home page
		return HttpResponse("You have been succesfully loginned!")

def logout_user(request):
		print "user logged out"
		logout(request)
		return redirect('/')

