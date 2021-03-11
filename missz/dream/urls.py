from django.urls import path

from . import views

urlpatterns = [
    path('', views.interpret_dream, name='interpret_dream'),
]