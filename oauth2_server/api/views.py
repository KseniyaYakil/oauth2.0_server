from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Position, Employe
from django.http.response import HttpResponse, Http404
from django.http import JsonResponse
from django import get_version

def position(request):
		positions = get_list_or_404(Position)
		return JsonResponse({
				'positions' : [obj.name for obj in positions]
		})

def index(request):
		return JsonResponse({
				'server': 'oauth2_server.com',
				'version': 'django {0}'.format(get_version())
		})
