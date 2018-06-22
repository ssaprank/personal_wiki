from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Article

import datetime

def index(request):
	return HttpResponse(request)

def show_page(request, page_id):
	get_object_or_404(Article, Id = page_id)
	return HttpResponse(request)
