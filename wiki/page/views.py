"""
Contains views of the page module
"""
import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings

from .models import Article, ArticleForm, Image, ImageForm, Tag
from .helpers import WikiStringHelper

HTML_TAG_ROW = ['a', 'b', 'i', 'ul', 'li', 'p', 'pre', 'code']
HTML_TAGS_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/static/page/html_tag_list.txt'
HTML_TAG_LIST = [x.replace("\n", "") for x in open(HTML_TAGS_FILE_PATH, 'r').readlines()]
SHORT_DESCRIPTION_LENGTH = 220

def index(request):
	"""Main view - list all pages"""
	template_name = 'page/home.html'

	pages = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]
	wip_pages = Article.objects.filter(work_in_progress=True)

	for page in pages:
		page.short_description = WikiStringHelper.get_article_short_description(
			page.html,
			SHORT_DESCRIPTION_LENGTH
			)

	render_params = {"greeting" : "", "pages" : pages, 'wip_pages' : wip_pages}
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
			page.short_description = WikiStringHelper.get_article_short_description(
				page.html,
				SHORT_DESCRIPTION_LENGTH
				)

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
	render_params = {"html_tag_list" : HTML_TAG_LIST, "html_tag_row" : HTML_TAG_ROW}
	render_params['images'] = Image.objects.all()
	render_params['base_dir'] = settings.BASE_DIR
	if request.method == 'POST':
		page_form = ArticleForm(request.POST, instance=page_object)
		hidden_tags_input = request.POST.get('hidden_page_tags_input', '')

		if page_form.is_valid():
			page_form.instance.last_modified = timezone.now()
			new_form_id = save_page_form(page_form, hidden_tags_input)

			# now check if tags that are associated with page are not presented in hidden_tags_input
			page_tags = Tag.objects.filter(articles__id=new_form_id)
			page_object = Article.objects.get(id=new_form_id)

			hidden_tags_input_list = hidden_tags_input.split(",")

			for page_tag in page_tags:
				if page_tag.name not in hidden_tags_input_list:
					page_object.tag_set.remove(page_tag)
					if page_tag.articles.all().count() == 0:
						page_tag.delete()

			return redirect('page:index')
		else:
			render_params['page_associated_tags'] = hidden_tags_input
			render_params['page_form'] = page_form
			render_params['form_errors'] = page_form.errors

			if hidden_tags_input:
				render_params['page_tags'] = hidden_tags_input.split(',')
				render_params['page_associated_tags'] = hidden_tags_input

			return render(request, template_name, render_params)
	else:
		render_params['page_tags'] = Tag.objects.filter(articles__id=page_object.id)
		render_params['page_form'] = ArticleForm(instance=page_object)
		render_params['page_associated_tags'] = ""

		for tag_object in render_params['page_tags']:
			render_params['page_associated_tags'] += tag_object.name + ","

		render_params['page_associated_tags'] = render_params['page_associated_tags'][:-1]

		return render(request, template_name, render_params)

def create_page(request):
	""" Renders view for creating a new page """
	template_name = 'page/edit_create_page.html'
	render_params = {"html_tag_list" : HTML_TAG_LIST, "html_tag_row" : HTML_TAG_ROW}
	render_params['images'] = Image.objects.all()
	render_params['base_dir'] = settings.BASE_DIR
	if request.method == 'POST':
		page_form = ArticleForm(request.POST)

		if page_form.is_valid():
			hidden_tags_input = request.POST.get('hidden_page_tags_input', '')
			save_page_form(page_form, hidden_tags_input)

			return redirect('page:index')
		else:
			render_params['page_form'] = page_form
			render_params['form_errors'] = page_form.errors
			hidden_tags_input = request.POST.get('hidden_page_tags_input', '')
			if hidden_tags_input:
				render_params['page_tags'] = hidden_tags_input.split(',')
				render_params['page_associated_tags'] = hidden_tags_input
			return render(request, template_name, render_params)
	else:
		render_params['page_form'] = ArticleForm()
		render_params['page_tags'] = {}
		return render(request, template_name, render_params)

def save_page_form(page_form, hidden_tags_input):
	"""Stores the article form along with its tags"""
	new_form = page_form.save()
	new_article = Article.objects.get(pk=new_form.pk)
	new_form_id = new_form.pk

	if hidden_tags_input is not "":
		for tag in hidden_tags_input.split(','):
			# if tag already exists
			if Tag.objects.filter(name=tag).count() > 0:
				existing_tag = Tag.objects.get(name=tag)
				# if tag is already associated with page do nothing
				if existing_tag.articles.filter(pk=new_form.pk).count() > 0:
					pass
				else:
					existing_tag.articles.add(new_article)
			else:
				# create new tag and append article to it
				new_tag = Tag(name=tag)
				new_tag.save()
				new_tag.articles.add(new_article)
	return new_form_id

def delete_page(request, page_id): # pylint: disable=unused-argument
	"""
	Deletes page by ID and redirects to index
	Also deletes its tags if they are not bound to any other page
	"""
	if Article.objects.filter(id=page_id).count() > 0:
		for tag in Tag.objects.filter(articles__id=page_id):
			if tag.has_one_article():
				tag.delete()
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
		tags = Tag.objects.filter(name__icontains=search_query)
		results = []
		if tags.count() > 0:
			for tag in tags:
				if tag.articles.filter(work_in_progress=False).count() > 0:
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

def get_last_uploaded_image(request):
	"""Renders the image that was uploaded last so it can be used for insertion"""
	if request.is_ajax():
		template_name = 'page/pieces/template_image_for_insertion.html'
		last_uploaded_image = Image.objects.order_by('-uploaded_at')[:1]
		# needed to get the object from queryset
		for img in last_uploaded_image:
			render_params = {'image' : img}
		return render(request, template_name, render_params)

def get_last_inserted_tag(request):
	"""Receives the tag name per ajax and renders bootstrap box to immediately show it on the page"""
	if request.is_ajax():
		tag_name = request.GET.get('tag_name', '')
		if tag_name:
			template_name = 'page/pieces/template_new_page_tag.html'
			render_params = {'tag_name' : tag_name}
			return render(request, template_name, render_params)
