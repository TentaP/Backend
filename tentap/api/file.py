import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django import forms

from tentap.serializers import FileSerializer
from tentap.models import File
from tentap.permissions import *

class UploadFileForm(forms.Form):
    file_name = forms.CharField(max_length=50)
    file = forms.FileField()

@api_view(['POST', 'GET'])
@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        file_data = JSONParser().parse(request)
        file_serializer = FileSerializer(data=file_data)
        if file_serializer.is_valid():
            file_serializer.save()
            return JsonResponse(file_serializer.data, status.HTTP_201_CREATED) 
        return JsonResponse(file_serializer.errors, status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        files = File.objects.all()
        file_serializer = FileSerializer(files, many=True)
        return JsonResponse(file_serializer.data, safe=False)

@api_view(['GET'])
def file(request, pk):
    files = File.objects.get(pk=pk)
    if request.method == 'GET':
        file_serializer = FileSerializer(file, many=False)
        return JsonResponse(file_serializer.data, safe=False)
