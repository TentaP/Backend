from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework import mixins

from django import forms

from tentap.serializers import FileSerializer, FileSearchSerializer
from tentap.models import File, Course, User
from tentap.permissions import *


"""
post request for the File model
"""
class fileUpload(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def post(self, request):

        user = get_user(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=user)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        #return JsonResponse({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class filePk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileSerializer
    Model = File
    queryset = Model.objects.all()

    def get(self, request, pk):
        try:
            file = self.queryset.get(pk=pk)
            serializer = self.serializer_class(file)
            return JsonResponse(serializer.data)
        except self.Model.DoesNotExist:
            return JsonResponse({'detail': 'file does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    """
    change file if normaluser is the author of the file
    Admin and Superuser can edit any file
    """
    def put(self, request, pk):

        user = get_user(request)

        try:
            file = self.queryset.get(pk=pk)
        except self.Model.DoesNotExist:
            return JsonResponse({'detail': 'file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not (user.is_admin or user.is_superuser) and file.uploaded_by != user:
            return JsonResponse({'detail': 'you are not the author'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(file, request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_user(request)
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return JsonResponse({'detail': 'file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not (user.is_admin or user.is_superuser) and file.uploaded_by != user:
            return JsonResponse({'detail': 'you are not the author'}, status=status.HTTP_401_UNAUTHORIZED)

        file.delete()
        return JsonResponse({},status=status.HTTP_204_NO_CONTENT)

class filesByCourse(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = FileSearchSerializer

    def get(self, request, course_name):
        try:
            course = Course.objects.get(course_name=course_name)
            files = course.Files.all()
            file_serializer = self.serializer_class(files, many=True)

            ## I changed this to get name instead of user id... can it effect anything else?
            ## TODO change this if needed
            for user_id in file_serializer.data:
                user_id['uploaded_by'] = User.objects.get(pk=user_id['uploaded_by']).username
            return JsonResponse(file_serializer.data, safe=False, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return JsonResponse({'detail': 'course does not exist'}, status=status.HTTP_404_NOT_FOUND)

class filesByUser(APIView):
    permissions_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = FileSearchSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'detail': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        files = user.Files.all()
        serializer = self.serializer_class(files, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
