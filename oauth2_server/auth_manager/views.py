from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from datetime import datetime
from .models import client_info, access_token, auth_code
from urlparse import urlparse
from uuid import uuid4

def get_client_id(client_app_id):
		try:
				client_app = get_object_or_404(client_info, client_id=client_app_id)
				return client_app
		except client_info.DoesNotExist:
				print("ERR: client with client_id {0} doesn't exist").format(client_app_id)
				return None

def get_err_response(params, err_msg):
		if 'redirect_uri' not in params or 'state' not in params:
				raise Http404
		return "{0}?error={1}&state={2}".format(params['redirect_uri'], err_msg, params['state'])

def parse_auth_req_params(request):
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
				auth_need_params = parse_auth_req_params(request)

		if request.method == 'GET' and request.session.get('has_access', None) is None:
				res = check_req_params(auth_need_params)
				if res !=  None:
						return redirect(get_err_response(auth_need_params, res))

				request.session['get_params'] = auth_need_params
				if request.user.is_authenticated():
						print "user authenticated. request access"
						print("%r", request.user)
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
		auth_code.objects.create(code=authorization_code, client_id=client_app, creation_time=datetime.now(), user=request.user)
		print "INF: Generated auth-on code {0} for client {1}".format(authorization_code, auth_need_params['client_name'])

		#form response to client 
		redirect_answer = "{0}/?code={1}&state={2}".format(auth_need_params['redirect_uri'],
												authorization_code, auth_need_params['state'])
		return redirect(redirect_answer)

#TODO: in a case of error return Json object with err_code and err_detailed
def parse_access_req_params(req_params):
		access_need_params = {'grant_type' : 0, 'client_id' : 0, 'client_secret' : 0, 'redirect_uri' : 0, 'code' : 0}

		for key, value in access_need_params.items():
				if key not in req_params:
						print("ERR: no authorization needed param `{0}'").format(key)
						return JsonResponse({
								'error' : "no parametr {0}".format(key),
						})
				access_need_params[key] = req_params[key]

		return access_need_params

@csrf_exempt
def get_access_token(request):
		if 'grant_type' not in request.POST:
				print "ERR: no grant_type field in req"
				return JsonResponse({
						'error': 'no grant_type field'
				})

		if request.POST['grant_type'] == 'authorization_code':
				access_params = parse_access_req_params(request.POST)

				for key, value in access_params.items():
						print "{0} -> {1}".format(key, value)

				#check authorization code
				try:
						authorization_code = auth_code.objects.get(code=access_params['code'])
				except auth_code.DoesNotExist:
						print "ERR: no auth code `{0}' in db".format(access_params['code'])
						return JsonResponse({
								'error' : "incorrect authorization code"
						})

				#check client id and secret in db
				client_app = None
				try:
						client_app = get_object_or_404(client_info,
														client_id=access_params['client_id'],
														client_secret=access_params['client_secret'])
				except DoesNotExist:
						print("ERR: client with client_id: {0} client_secret: {1} doesn't exist").format(
																				access_params['client_id'],
																				access_params['client_secret'])
						return JsonResponse({
								'error': 'incorrect filed(s) client_id, client_secret'
						})

				if authorization_code.client_id != client_app:
						print "ERR: diff client_id and auth_code.client_id"
						raise Http404

				#check redirect uri
				if client_app.redirect_domain != access_params['redirect_uri']:
						print "ERR: redirect_uri {0} is not correct".format(access_params['redirect_uri'])
						return JsonResponse({
								'error': 'incorrect redirect uri for specified client'
						})

				#create refresh and access tokens
				req_refresh_token = generate_code()
				req_access_token = generate_code()

				print "INF: created tokens: access: {0} refresh: {1}".format(req_access_token, req_refresh_token)

				token = access_token.objects.create(token=req_access_token, app_id=client_app,
														refresh_token=req_refresh_token, user=authorization_code.user)
		elif request.POST['grant_type'] == 'refresh_token':
				req_refresh_token = request.POST['refresh_token'] if 'refresh_token' in request.POST else None
				if req_refresh_token is None:
						print "ERR: no field `refresh_token' in req"
						return JsonResponse({
								'error': 'no field refresh_token'
						})

				#check if refresh token is in db
				try:
						token = access_token.objects.get(refresh_token=req_refresh_token)
				except access_token.DoesNotExist:
						print "ERR: no refresh_token `{0}' in db".format(req_refresh_token)
						return JsonResponse({
								'error': 'incorrect refresh_token'
						})
				#generate new aceess token
				req_access_token = generate_code()

				#update db with new access_token
				token.token = req_access_token
				token.creation_time = datetime.now()
				token.save()

				print "INF: generated new access_token {0}".format(req_access_token)
		else:
				print "ERR: incorrect grant_type"
				return JsonResponse({
						'error': 'incorrect grant_type'
				})

		return JsonResponse({
				'access_token': token.token,
				'token_type' : 'bearer',
				'expires_in' : token.expires_in(),
				'refresh_token': token.refresh_token,
		})

