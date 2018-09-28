"""Handles url resolving and naming"""
from django.urls import path, re_path

from . import views

app_name = 'page' #pylint: disable=invalid-name

urlpatterns = [ #pylint: disable=invalid-name
    path('', views.index, name='index'),
    path('<int:page_id>/edit', views.edit_page, name='edit'),
    path('<int:page_id>/', views.show_page, name='show'),
    path('create', views.create_page, name='create'),
    path('<int:page_id>/delete', views.delete_page, name='delete'),
    re_path(r'^api/get_page_tags/', views.get_page_tags, name='get_page_tags'),
    re_path(r'^api/get_search_pages/', views.show_search_list, name='show_search_list'),
    re_path(r'^api/upload_image/', views.upload_image, name='upload_image'),
    re_path(r'^api/get_last_uploaded_image/', views.get_last_uploaded_image, name='get_last_uploaded_image'),
    re_path(r'^api/get_last_inserted_tag/', views.get_last_inserted_tag, name='get_last_inserted_tag'),
]
