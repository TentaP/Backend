from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello woorld, lets get em free exam solutions")


