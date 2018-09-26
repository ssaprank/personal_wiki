"""
Contains views of the page module
"""
import json
import os
import base64
import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import Article, ArticleForm, Image, ImageForm, Tag
from .helpers import WikiStringHelper

html_tag_row = ['a', 'b', 'h1', 'h5', 'i', 'strong']
file_path = os.path.dirname(os.path.realpath(__file__)) + '/static/page/html_tag_list.txt'
html_tag_list = list(map(lambda s: s.replace("\n",""), open(file_path, 'r').readlines()))

def index(request):
	"""Main view - list all pages"""
	template_name = 'page/home.html'

	pages = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]

	for page in pages:
		page.short_description = WikiStringHelper.get_article_short_description(page.html, 50)

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
			filters['tag__name__icontains'] = tag_term
		if title_term != '':
			filters['title__icontains'] = title_term

		pages = Article.objects.filter(**filters).order_by('-last_modified')[:5]

		for page in pages:
			page.short_description = WikiStringHelper.get_article_short_description(page.html, 50)

		render_params = {"pages" : pages}
		return render(request, template_name, render_params)
	else:
		return redirect('page:index')

def show_page(request, page_id):
	"""Show page by id"""
	page_object = get_object_or_404(Article, id=page_id)
	template_name = 'page/show_page.html'
	render_params = {"page_object" : page_object}
	return render(request, template_name, render_params)

def edit_page(request, page_id):
	"""Returns view that allows to edit page by its ID"""
	page_object = get_object_or_404(Article, id=page_id)
	template_name = 'page/edit_create_page.html'
	render_params = {"html_tag_list" : html_tag_list, "html_tag_row" : html_tag_row}
	render_params['images'] = Image.objects.all()
	render_params['base_dir'] = settings.BASE_DIR
	if request.method == 'POST':
		page_form = ArticleForm(request.POST, instance=page_object)
		if page_form.is_valid():
			page_form.instance.last_modified = timezone.now()
			page_form.save()
			return redirect('page:index')
		else:
			render_params['page_form'] = page_form
			render_params['form_errors'] = page_form.errors
			return render(request, template_name, render_params)
	else:
		render_params['page_form'] = ArticleForm(instance=page_object)
		return render(request, template_name, render_params)

def create_page(request):
	""" Renders view for creating a new page """
	template_name = 'page/edit_create_page.html'
	render_params = {"html_tag_list" : html_tag_list, "html_tag_row" : html_tag_row}
	render_params['images'] = Image.objects.all()
	render_params['base_dir'] = settings.BASE_DIR
	if request.method == 'POST':
		page_form = ArticleForm(request.POST)
		if page_form.is_valid():
			page_form.save()
			return redirect('page:index')
		else:
			render_params['page_form'] = page_form
			render_params['form_errors'] = page_form.errors
			return render(request, template_name, render_params)
	else:
		render_params['page_form'] = ArticleForm()
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
		search_query = request.GET.get('term', '')
		tags = Tag.objects.filter(name__icontains=search_query).only('name')
		results = []
		for tag in tags:
			results.append(tag.name)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, mimetype)

def upload_image(request):
	"""
	Handles uploading images in edit_create_page
	"""
	form = ImageForm(request.POST, request.FILES)
	if form.is_valid():
		image = form.save()
		data = {'is_valid' : True, 'url' : image.image.url}
	else:
		data = {'is_valid' : False}
	return JsonResponse(data)

def set_page_tag(request):
	"""
	gets page id and tag name
	checks whether tag exists: if not creates it
	checks whether tag is already bound to this page: if not bounds it
	"""