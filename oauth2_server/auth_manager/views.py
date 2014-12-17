from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from datetime import datetime
from .models import client_info, access_token, auth_code
from urlparse import urlparse
from uuid import uuid4

def get_client_id(client_app_id):
		try:
				client_app = get_object_or_404(client_info, client_id=client_app_id)
				return client_app
		except DoesNotExist:
				print("ERR: client with client_id {0} doesn't exist").format(client_app_id)
				return None

def get_err_response(params, err_msg):
		if 'redirect_uri' not in params or 'state' not in params:
				raise Http404
		return "{0}?error={1}&state={2}".format(params['redirect_uri'], err_msg, params['state'])

def parse_req_params(request):
		auth_need_params = {'response_type' : 0, 'client_id' : 0, 'redirect_uri' : 0, 'state' : 0}
		for key, value in auth_need_params.items():
				if key not in request.GET:
						print("ERR: no authorization needed param `{0}'").format(key)
						raise Http404
				if key == 'response_type' and request.GET[key] != 'code':
						print("ERR: recv response_type = {0} (MUST be 'code')").format(value)
						raise Http404
				auth_need_params[key] = request.GET[key]

		return auth_need_params

def check_req_params(auth_need_params):
		client_app = get_client_id(auth_need_params['client_id'])
		if client_app is None:
				return 'no_client'

		auth_need_params['client_name'] = client_app.client_name

		print auth_need_params['client_name']

		if urlparse(auth_need_params['redirect_uri']).netloc != urlparse(client_app.redirect_domain).netloc:
				print "ERR: no specified domain in db"
				return 'incorrect_redirect_domain'

		return None

def generate_code():
    return uuid4().hex

@csrf_exempt
def auth_code_req(request):
		if 'redirect_internal' in request.session:
				del request.session['redirect_internal']

		if 'get_params' in request.session:
				request.GET = request.session['get_params']
				del request.session['get_params']
				auth_need_params = request.GET
		else:
				auth_need_params = parse_req_params(request)

		if request.method == 'GET' and request.session.get('has_access', None) is None:
				res = check_req_params(auth_need_params)
				if res !=  None:
						return redirect(get_err_response(auth_need_params, res))

				request.session['get_params'] = auth_need_params
				if request.user.is_authenticated():
						print "user authenticated. request access"
						return render(request, 'auth_manager/access.html', {'app_name' : auth_need_params['client_name']})
				else:
						print "ask for logging in"
						request.session['redirect_internal'] = '/auth'
						return redirect('/user/login_user/')

		if 'has_access' not in request.POST:
				print "ERR: no field `has access'"
				raise Http404

		if request.POST['has_access'] == 'No':
				print("INF: user denied acces request for client {0}").format(auth_need_params['client_name'])
				return redirect(get_err_response(auth_need_params, 'user_denied_access_request'))

		#generate authorization code
		client_app = get_client_id(auth_need_params['client_id']);
		if client_app is None:
				print "ERR: can not find client with id {0}".format(auth_need_params['client_id'])
				raise Http404

		authorization_code = generate_code()
		auth_code.objects.create(code=authorization_code, client_id=client_app, creation_time=datetime.now())
		print "INF: Generated auth-on code {0} for client {1}".format(authorization_code, auth_need_params['client_name'])

		#form response to client 
		redirect_answer = "{0}/?code={1}&state={2}".format(auth_need_params['redirect_uri'],
												authorization_code, auth_need_params['state'])
		return redirect(redirect_answer)

