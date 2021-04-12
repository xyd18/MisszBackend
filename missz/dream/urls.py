from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.check_times, name='check_times'),
    path('all/', views.all_dream, name='all_dream'),
    path('', views.interpret_dream, name='interpret_dream')
]