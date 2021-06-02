from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    path('user/', views.check_times, name='check_times'),
    path('all/', views.all_dream, name='all_dream'),
    path('similar/', views.similar_dream, name='similar_dream'),
    path('good/', views.get_good, name='get_good'),
    path('bad/', views.get_bad, name='get_bad'),
    path('image/', views.get_image, name='get_image'),
    path('', views.interpret_dream, name='interpret_dream'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]