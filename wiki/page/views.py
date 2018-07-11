from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Article, ArticleForm

import datetime

def index(request):
	template_name = 'page/index.html'
	
	last_five_modified = Article.objects.filter(work_in_progress=False).order_by('-last_modified')[:5]

	render_params = {"greeting" : "hello", "last_modified" : last_five_modified}
	return render(request, template_name, render_params)

def show_page(request, page_id):
	page_object = get_object_or_404(Article, id = page_id)
	if page_object.tags is not None:
		page_object.tags = page_object.tags.split(",")
	template_name = 'page/show_page.html'
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
