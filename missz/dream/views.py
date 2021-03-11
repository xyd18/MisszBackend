from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def interpret_dream(request):
    return HttpResponse("Hello, world. You're at the polls index.")