from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core import serializers

from .models import Article, ArticleForm

import datetime
import json

def index(request):
	template_name = 'page/index.html'
	
	pages = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]

	render_params = {"greeting" : "hello", "pages" : pages}
	return render(request, template_name, render_params)

def show_search_list(request):
	if request.is_ajax():
		element = request.GET.get('search_element', '')
		term = request.GET.get('term', '')
		template_name = 'page/page_list.html'

		if term != '':
			if element == 'tag':
				pages = Article.objects.filter(work_in_progress=False,tags__icontains=term).order_by('-last_modified')[:5]
			elif element == 'title':
				pages = Article.objects.filter(work_in_progress=False,title__icontains=term).order_by('-last_modified')[:5]
		else:
			pages = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]

		render_params = {"pages" : pages}
		return render(request, template_name, render_params)
	else:
		return redirect('page:index')

def show_page(request, page_id):
	page_object = get_object_or_404(Article, id = page_id)
	template_name = 'page/show_page.html'
	if page_object.tags is not None:
		page_object.tags = page_object.tags.split(',')
	render_params = {"page_object" : page_object}
	return render(request, template_name, render_params)

def edit_page(request, page_id):
	page_object = get_object_or_404(Article, id = page_id)
	template_name = 'page/edit_create_page.html'
	if (request.method == 'POST'):
		page_form = ArticleForm(request.POST, instance=page_object)
		if (page_form.is_valid()):
			page_form.instance.last_modified = timezone.now()
			page_form.save()
			return redirect('page:index')
		else:
			form_errors = page_form.errors
			return render(request, template_name, {"page_form" : page_form, "form_errors" : form_errors})
	else:
		page_form = ArticleForm(instance=page_object)
		render_params = {"page_form" : page_form}
		return render(request, template_name, render_params)

def create_page(request):
	template_name = 'page/edit_create_page.html'
	if (request.method == 'POST'):
		page_form = ArticleForm(request.POST)
		if (page_form.is_valid()):
			page_form.save()
			return redirect('page:index')
		else:
			form_errors = page_form.errors
			return render(request, template_name, {"page_form" : page_form, "form_errors" : form_errors})
	else:
		page_form = ArticleForm()
		render_params = {"page_form" : page_form}
		return render(request, template_name, render_params)

def delete_page(request, page_id):
	Article.objects.filter(id=page_id).delete()
	return redirect('page:index')

def get_page_tags(request):
	mimetype = 'application/json'
	if request.is_ajax():
		search_query = request.GET.get('term', '').replace(",", "")
		pages = Article.objects.filter(tags__icontains = search_query)[:5]
		results = []
		for page in pages:
			tags = (tag for tag in page.tags.split(",") if tag not in results and search_query in tag)
			for tag in tags:
				results.append(tag)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, mimetype)

