from django.urls import path, re_path

from . import views

app_name = 'page'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_id>/edit', views.edit_page, name='edit'),
    path('<int:page_id>/', views.show_page, name='show'),
    path('create', views.create_page, name='create'),
    path('<int:page_id>/delete', views.delete_page, name='delete'),
    re_path(r'^api/get_page_tags/', views.get_page_tags, name='get_page_tags'),
    re_path(r'^api/get_search_pages/', views.show_search_list, name='show_search_list')
]