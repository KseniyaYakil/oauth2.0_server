from django.http import HttpResponse
from django.shortcuts import render

def home(request):
		return render(request, 'oauth2_server/home.html')
