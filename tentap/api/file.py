from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import  JsonResponse

from django import forms

from tentap.serializers import FileSerializer, FileSearchSerializer
from tentap.models import File, Course, User
from tentap.permissions import *

"""
post request for the File model
"""
class fileUpload(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = (MultiPartParser, )
    serializer_class = FileSerializer

    # TODO: fix post
    def post(self, request):
        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        #file_serializer = FileSerializer(data=file_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)


class filePk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = [MultiPartParser, ]
    serializer_class = FileSerializer
    Model = File
    queryset = Model.objects.all()

    def get(self, request, pk):
        try:
            file = self.queryset.get(pk=pk)
            serializer = self.serializer_class(file)
            return JsonResponse(serializer.data)
        except self.Model.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)
    
    """
    change file if normaluser is the author of the file
    Admin and Superuser can edit any file
    """
    def put(self, request, pk):

        user = get_user(request)

        try:
            file = self.queryset.get(pk=pk)
        except self.Model.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

        if not (user.is_admin or user.is_superuser) and file.author != user.pk:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = self.serializer_class(file, request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except self.Model.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = get_user(request)
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

        if not (user.is_admin or user.is_superuser) and file.author != user.pk:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED)

        file.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

class filesByCourse(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = FileSearchSerializer

    def get(self, request, course):
        try:
            course = Course.objects.get(course_name=course)
            files = course.Files.all()
            file_serializer = self.serializer_class(files, many=True)
            return JsonResponse(file_serializer.data, safe=False, status=status.HTTP_200_OK)
        except Course.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

class filesByUser(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = FileSearchSerializer

    def get(self, request):
        user = get_user(request)
        try:
            files = user.Files.all()
            serializer = self.serializer_class(files, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except File.DoesNotExist as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)
