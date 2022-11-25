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

from tentap.serializers import FileSerializer, FileForm
from tentap.models import File
from tentap.permissions import *

"""
post request for the File model
"""
class fileupload(APIView):
    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        #file_serializer = FileSerializer(data=file_data)
        if form.is_valid():
            instance = File(file=request.FILES['file'])
            instance.save()
            return JsonResponse(instance.data, status.HTTP_201_CREATED) 
        return JsonResponse(form.errors, status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        files = File.objects.all()
        file_serializer = FileSerializer(files, many=True)
        return JsonResponse(file_serializer.data, safe=False)

@api_view(['GET'])
def file(request, pk):
    files = File.objects.get(pk=pk)
    if request.method == 'GET':
        file_serializer = FileSerializer(file, many=False)
        return JsonResponse(file_serializer.data, safe=False)
