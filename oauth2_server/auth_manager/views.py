from django.shortcuts import render, redirect
from config import AuthConf
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

#access_token request

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

				#check redirect uri
				#TODO: rename app_name with real application name
				if request.user.is_authenticated():
						print "user authenticated. request access"
						return render(request, 'auth_manager/access.html', {'app_name' : 'test_app'})
				else:
						request.session['redirect_internal'] = '/auth'
						request.session['stored_auth_params'] = auth_need_params
						return redirect('/user/login_user/')

		if request.method == 'GET' and has_auth_params and request.user.is_authenticated():
				print "user authenticated. request access"
				return render(request, 'auth_manager/access.html', {'app_name' : 'test_app'})

		for param  in request.POST.items():
				print("post : {0}").format(param)

		if has_auth_params:
				for param  in request.session['stored_auth_params'].items():
						print("get params: {0}").format(param)
		else:
				for param  in request.GET.items():
						print("get : {0}").format(param)

		request.session['stored_auth_params'].clear()
		if 'has_access' not in request.POST:
				print "ERR: no field `has access'"
				raise Http404

		return HttpResponse("user succesfully logged in")

