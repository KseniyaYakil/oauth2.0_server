from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Position, Employe
from django.http.response import HttpResponse, Http404
from django.http import JsonResponse
from django import get_version
import json
import httplib2
from django.views.decorators.csrf import csrf_exempt
from auth_manager.models import auth_code, access_token, client_info

#public method

@csrf_exempt
def position(request):
		positions = get_list_or_404(Position)
		return JsonResponse({
				'positions' : [obj.name for obj in positions]
		})

def check_access(request, access_token_obj):
		access_token_obj = None

		for header in request.META:
				print "api req: {0} -> {1}".format(header, request.META[header])

		if 'HTTP_AUTHORIZATION' not in request.META:
				return 'no authorization field'

		access_code = request.META['HTTP_AUTHORIZATION']
		#check if access token is correct
		try:
				acc_obj = access_token.objects.get(token=access_code)
		except access_token.DoesNotExist:
				return 'incorrect auth code'

		#check if auth_code is not expired
		if acc_obj.is_expired():
				return 'access_token is expired'

		access_token_obj = acc_obj
		return 'ok'


#for authorized users
@csrf_exempt
def me(request):
		access_token_obj = None
		msg = check_access(request, access_token_obj)
		if msg == 'ok':
				#get user correctly! 
				#get token object -> get client
				user = request.user
				return JsonResponse({
						#'full_name': user.first_name,
						'username': user.username,
						#'email': user.email,
						#'mobile_phone': user.mobile_phone,
						#'birthday': user.birth_day
				})
		else:
				return JsonResponse({
						'error': msg
				})

@csrf_exempt
def employes(request):
		access_token_obj = None
		msg = check_access(request, access_token_obj)
		if msg == 'ok':
				return JsonResponse({
						'status' : 'ok'
				})
		else:
				return JsonResponse({
						'error': msg
				})

@csrf_exempt
def employe_id(request, emp_id):
		print emp_id
		access_token_obj = None
		msg = check_access(request, access_token_obj)
		if msg == 'ok':
				#get user id 
				#if user id == emp id 
				return JsonResponse({
						'status' : 'ok'
				})
		else:
				return JsonResponse({
						'error': msg
				})

@csrf_exempt
def position_id(request, pos_id):
		print pos_id
		access_token_obj = None
		msg = check_access(request)
		if msg == 'ok':
				#get employe info 

				#if employe pos_id == id
				return JsonResponse({
						'status' : 'ok'
				})
		else:
				return JsonResponse({
						'error': msg
				})

def index(request):
		return JsonResponse({
				'server': 'oauth2_server.com',
				'version': 'django {0}'.format(get_version())
		})
