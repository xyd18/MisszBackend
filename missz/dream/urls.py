from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.check_times, name='check_times'),
    path('all/', views.all_dream, name='all_dream'),
    path('similar/', views.similar_dream, name='similar_dream'),
    path('good/', views.get_good, name='get_good'),
    path('bad/', views.get_bad, name='get_bad'),
    path('', views.interpret_dream, name='interpret_dream')
]