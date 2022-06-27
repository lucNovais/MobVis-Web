from django.urls import path

from . import views

app_name = 'frontpage'

urlpatterns = [
    path('', views.starting_page, name='home'),
    path('demo/', views.demo_page, name='demo')
]