from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Position, Employe
from django.http.response import HttpResponse, Http404
from django.http import JsonResponse
from django import get_version
import json
import httplib2
from django.views.decorators.csrf import csrf_exempt
from auth_manager.models import auth_code, access_token, client_info
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .config import ApiConfig

#paginator
def paginate(page_number, objs):
		paginator = Paginator(objs, ApiConfig.paginator_items_per_page)
		try:
				return paginator.page(page_number)
		except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				return paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				return None

#public method
@csrf_exempt
def position(request):
		if 'page' in request.GET:
				page = paginate(request.GET['page'], Position.objects.all())
				if page is None:
						resp = HttpResponse()
						resp.status_code = 500
						return resp

				objects = page.object_list
		else:
				objects = get_list_or_404(Position)

		position_list = [{'id': obj.id, 'name' : obj.name} for obj in objects]

		response_data = {}
		response_data['items_cnt'] = len(position_list)
		response_data['positions'] = position_list

		resp = HttpResponse(json.dumps(response_data), content_type="application/json")
		resp.status_code = 200

		return resp

def check_access(request):
		for header in request.META:
				print "api req: {0} -> {1}".format(header, request.META[header])

		if 'HTTP_AUTHORIZATION' not in request.META:
				return 'no authorization field'

		access_code_str = request.META['HTTP_AUTHORIZATION']

		list_params = access_code_str.split(' ')
		if len(list_params) < 2:
				return 'incorrect access token'

		if list_params[0] != 'bearer':
				return 'incorrect access token'

		access_code = list_params[1]

		#check if access token is correct
		try:
				acc_obj = access_token.objects.get(token=access_code)
		except access_token.DoesNotExist:
				return 'incorrect auth code'

		#check if auth_code is not expired
		if acc_obj.is_expired():
				return 'access_token is expired'

		return 'ok'

#for authorized users
@csrf_exempt
def me(request):
		msg = check_access(request)
		if msg == 'ok':
				access_code = request.META['HTTP_AUTHORIZATION']
				acc_obj = access_token.objects.get(token=access_code)
				user = acc_obj.user

				response_data = {}
				response_data['full_name'] = user.first_name
				response_data['username'] = user.username
				response_data['email'] = user.email
				response_data['mobile_phone'] = user.mobile_phone
				response_data['birthday'] = user.birth_day

				resp = HttpResponse(json.dumps(response_data), content_type="application/json")
				resp.status_code = 200

				return resp
		else:
				print "ERR: {0}".format(msg)
				resp = HttpResponse()
				resp.status_code = 401
				return resp

@csrf_exempt
def employes(request):
		msg = check_access(request)
		if msg == 'ok':
				if 'page' in request.GET:
						page = paginate(request.GET['page'], Employe.objects.all())
						if page is None:
								resp = HttpResponse()
								resp.status_code = 500
								return resp

						objects = page.object_list
				else:
						objects = get_list_or_404(Employe)

				employe_list = ["emp: {0} position: {1} id: {2}".format(obj.user.first_name,
																				obj.position.name,
																				obj.user.id) for obj in objects]
				response_data = {}
				response_data['items_cnt'] = len(employe_list)
				response_data['employes'] = employe_list

				resp = HttpResponse(json.dumps(response_data), content_type="application/json")
				resp.status_code = 200
				return resp
		else:
				resp = HttpResponse()
				resp.status_code = 401
				return resp

@csrf_exempt
def employe_id(request, emp_id):
		msg = check_access(request)
		if msg == 'ok':
				access_code = request.META['HTTP_AUTHORIZATION']
				acc_obj = access_token.objects.get(token=access_code)
				user = acc_obj.user

				str_user_id = "{0}".format(user.id)
				str_emp_id = "{0}".format(emp_id)
				if str_user_id != str_emp_id:
						resp = HttpResponse()
						resp.status_code = 403
						return resp
				try:
						emp_obj = Employe.objects.get(user=emp_id)
				except Employe.DoesNotExist:
						raise Http404

				position = emp_obj.position
				response_data = {}
				response_data['full_name'] = user.first_name
				response_data['username'] = user.username
				response_data['email'] = user.email
				response_data['mobile_phone'] = user.mobile_phone
				response_data['birthday'] = user.birth_day
				response_data['position'] = position.name

				resp = HttpResponse(json.dumps(response_data), content_type="application/json")
				resp.status_code = 200
				return resp
		else:
				resp = HttpResponse()
				resp.status_code = 401
				return resp

@csrf_exempt
def position_id(request, pos_id):
		msg = check_access(request)
		if msg == 'ok':
				access_code = request.META['HTTP_AUTHORIZATION']
				acc_obj = access_token.objects.get(token=access_code)
				user = acc_obj.user
				str_user_id = "{0}".format(user.id)
				str_pos_id = "{0}".format(pos_id)

				if str_user_id != str_pos_id:
						resp = HttpResponse()
						resp.status_code = 403
						return resp
				try:
						emp_obj = Employe.objects.get(user=pos_id)
				except Employe.DoesNotExist:
						raise Http404

				position = emp_obj.position
				response_data = {}
				response_data['full_name'] = user.first_name
				response_data['position_name'] = position.name
				response_data['salary'] = position.salary
				response_data['salary_currency'] = position.salary_currency

				resp = HttpResponse(json.dumps(response_data), content_type="application/json")
				resp.status_code = 200
				return resp
		else:
				resp = HttpResponse()
				resp.status_code = 401
				return resp

def index(request):
		response_data = {}
		response_data['server'] = 'oauth2_server.com'
		response_data['version'] = 'django {0}'.format(get_version())

		resp = HttpResponse(json.dumps(response_data), content_type="application/json")
		resp.status_code = 200
		return resp

