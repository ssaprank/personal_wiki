from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Article, ArticleForm
from django.forms import modelformset_factory

import datetime

def index(request):
	template_name = 'page/index.html'

	last_five_pages = Article.objects.order_by('last_modified')[:5]

	render_params = {"greeting" : "hello", "lastPages" : last_five_pages}
	return render(request, template_name, render_params)

def show_page(request, page_id):
	get_object_or_404(Article, Id = page_id)
	return HttpResponse(request)

def create_page(request)
	ArticleFormSet = modelformset_factory(Article, fields=('title', 'html'))
	if (request.method == 'POST'):
		formset = ArticleFormSet(request.POST)
		if (formset.is_valid()):
			return redirect('page:index')
		else:
			#return error message
	else:
		template_name = 'page/create_page.html'
		return render(request, template_name)
