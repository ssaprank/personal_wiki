"""
Contains views of the page module
"""
import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Article, ArticleForm

html_tag_row = ['a', 'b', 'h1', 'h5', 'i', 'strong']

def index(request):
	"""Main view - list all pages"""
	template_name = 'page/index.html'

	pages = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]

	render_params = {"greeting" : "hello", "pages" : pages}
	return render(request, template_name, render_params)

def show_search_list(request):
	"""Show list of pages using search parameters from the search fields"""
	if request.is_ajax():
		tag_term = request.GET.get('tag_term', '')
		title_term = request.GET.get('title_term', '')
		template_name = 'page/page_list.html'

		filters = {'work_in_progress' : False}

		if tag_term != '':
			filters['tags__icontains'] = tag_term
		if title_term != '':
			filters['title__icontains'] = title_term

		pages = Article.objects.filter(**filters).order_by('-last_modified')[:5]

		render_params = {"pages" : pages}
		return render(request, template_name, render_params)
	else:
		return redirect('page:index')

def show_page(request, page_id):
	"""Show page by id"""
	page_object = get_object_or_404(Article, id=page_id)
	template_name = 'page/show_page.html'
	if page_object.tags is not None:
		page_object.tags = page_object.tags.split(',')
	render_params = {"page_object" : page_object}
	return render(request, template_name, render_params)

def edit_page(request, page_id):
	"""Returns view that allows to edit page by its ID"""
	page_object = get_object_or_404(Article, id=page_id)
	storage_class = get_storage_class(settings.STATICFILES_STORAGE)
	template_name = 'page/edit_create_page.html'
	if request.method == 'POST':
		page_form = ArticleForm(request.POST, instance=page_object)
		if page_form.is_valid():
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
	""" Renders view for creating a new page """
	template_name = 'page/edit_create_page.html'
	file_path = os.path.dirname(os.path.realpath(__file__)) + '/static/page/html_tag_list.txt'
	html_tag_list = list(map(lambda s: s.replace("\n",""), open(file_path, 'r').readlines()))
	if request.method == 'POST':
		page_form = ArticleForm(request.POST)
		if page_form.is_valid():
			page_form.save()
			return redirect('page:index')
		else:
			form_errors = page_form.errors
			return render(request, template_name, {"page_form" : page_form, "form_errors" : form_errors, "html_tag_list" : html_tag_list, "html_tag_row" : html_tag_row})
	else:
		page_form = ArticleForm()
		render_params = {"page_form" : page_form, "html_tag_list" : html_tag_list, "html_tag_row" : html_tag_row}
		return render(request, template_name, render_params)

def delete_page(request, page_id): # pylint: disable=unused-argument
	""" Deletes page by ID and redirects to index """
	Article.objects.filter(id=page_id).delete()
	return redirect('page:index')

def get_page_tags(request):
	"""
	Returns ajax response containing tags
	based on the first two letters in the search autocomplete
	"""
	mimetype = 'application/json'
	if request.is_ajax():
		search_query = request.GET.get('term', '').replace(",", "")
		pages = Article.objects.filter(tags__icontains=search_query)[:5]
		results = []
		for page in pages:
			tags = (tag for tag in page.tags.split(",") if tag not in results and search_query in tag)
			for tag in tags:
				results.append(tag)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, mimetype)
