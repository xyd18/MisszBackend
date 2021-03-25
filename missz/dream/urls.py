from django.urls import path

from . import views

urlpatterns = [
    path('/user', views.check_times, name='check_times'),
    path('', views.interpret_dream, name='interpret_dream')
]