from django.urls import path

from . import views

app_name = 'page'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_id>/', views.show_page, name='show'),
    path('create', views.create_page, name='create')
]