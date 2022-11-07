from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello world, lets get em free exam solutions")


