from django.shortcuts import render
from config import AuthConf
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

#access_token request

#TODO: add 'state' parametr 
@csrf_exempt
def auth_code_req(request):
		if request.method == 'GET':
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

				return render(request, 'auth_manager/login_and_access.html', {'app_name' : 'test_app'})

		for param  in request.POST.items():
				print("post : {0}").format(param)

		for param  in request.GET.items():
				print("get : {0}").format(param)


		if 'has_access' not in request.POST:
				print "ERR: no field `has access'"
				raise Http404

		return HttpResponse("user succesfully logged in")

