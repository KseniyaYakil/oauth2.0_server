from django.shortcuts import render, redirect, get_object_or_404
from config import AuthConf
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .models import client_info, access_token
from urlparse import urlparse

#access_token request

def check_client_id(client_app_id):
		try:
				client_app = get_object_or_404(client_info, client_id=client_app_id)
				return client_app
		except DoesNotExist:
				print("ERR: client with client_id {0} doesn't exist").format(client_app_id)
				return None

#TODO: add 'state' parametr 
@csrf_exempt
def auth_code_req(request):
		has_auth_params = 0
		if 'stored_auth_params' in request.session and request.session['stored_auth_params']:
				has_auth_params = 1

		if request.method == 'GET' and not has_auth_params:
				auth_need_params = {'response_type' : 0, 'client_id' : 0, 'redirect_uri' : 0}

				#extract needed parametrs
				for key, value in auth_need_params.items():
						if key not in request.GET:
								print("ERR: no authorization needed param `{0}'").format(key)
								raise Http404
						if key == 'response_type' and request.GET[key] != 'code':
								print("ERR: recv response_type = {0} (MUST be 'code')").format(value)
								raise Http404

						auth_need_params[key] = request.GET[key]

				#check client_id in data base
				client_app = check_client_id(auth_need_params['client_id'])
				if client_app is None:
						return redirect('{0}?error=no_client'.format(auth_need_params['client_id']))
				auth_need_params['client_name'] = client_app.client_name

				#check redirect uri
				if urlparse(auth_need_params['redirect_uri']).netloc != urlparse(client_app.redirect_domain).netloc:
						print "ERR: no specified domain in db"
						return redirect("{0}/?error=incorrect_domain".format(auth_need_params['redirect_uri']))

				if request.user.is_authenticated():
						print "user authenticated. request access"
						return render(request, 'auth_manager/access.html', {'app_name' : client_app.client_name})
				else:
						print "ask for logging in"
						request.session['redirect_internal'] = '/auth'
						request.session['stored_auth_params'] = auth_need_params
						return redirect('/user/login_user/')

		auth_need_params = request.GET if has_auth_params == 0 else request.session['stored_auth_params']

		if request.method == 'GET' and has_auth_params and request.user.is_authenticated():
				return render(request, 'auth_manager/access.html', {'app_name' : auth_need_params['client_name']})

		for param  in request.POST.items():
				print("post : {0}").format(param)
		for param  in auth_need_params.items():
				print("get : {0}").format(param)


		request.session['stored_auth_params'].clear()
		#TODO: set correctly variable 'has_access' in form
		if 'has_access' not in request.POST:
				print "ERR: no field `has access'"
				raise Http404

		return HttpResponse("user succesfully logged in")

