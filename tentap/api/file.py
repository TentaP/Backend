import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django import forms

from tentap.serializers import FileSerializer
from tentap.models import File, Course, User
from tentap.permissions import *

"""
post request for the File model
"""
class fileUpload(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = (MultiPartParser, )
    serializer_class = FileSerializer

    def post(self, request):
        user = get_user(request)
        request.data['uploaded_by'] = user.pk
        request.data['at_university'] = user.university.pk
        request.data['course'] = int(request.data['course'])
        serializer = self.serializer_class(data=request.data)
        #file_serializer = FileSerializer(data=file_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status.HTTP_201_CREATED) 
        print (serializer.errors)
        return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)


class filePk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def get(self, request, pk):
        try:
            file = File.objects.get(pk=pk)
            serializer = FileSerializer(file)
            return Response(serializer.data)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    """
    change file if normaluser is the author of the file
    Admin and Superuser can edit any file
    """
    def put(self, request, pk):
        if isNormalUser and get_user(request) != file.author:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            data = JSONParser().parse(request)
            file = File.objects.get(pk=pk)
            serializer = FileSerializer(file, data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            file = File.objects.get(pk=pk)
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class filesByCourse(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]

    def get(self, request, course):
        try:
            course = Course.objects.get(course_name=course)
            files = course.files.all()
            file_serializer = FileSerializer(files, many=True)
            return JsonResponse(file_serializer.data, safe=False)
        except Course.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

class filesByUser(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = FileSerializer

    def get(self, request):
        try:
            user = get_user(request)
            try:
                files = user.Reviews.all()
                serializer = self.serializer_class(files, many=True)
                return JsonResponse(file_serializer.data, safe=False)
            except File.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
