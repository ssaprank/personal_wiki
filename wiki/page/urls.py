from django.urls import path

from . import views

app_name = 'page'
urlpatterns = [
    path('', views.index),
    path('<int:page_id>/', views.show_page)
]