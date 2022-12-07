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

from tentap.serializers import UsersSerializer, CourseSerializer
from tentap.models import Course, University
from tentap.permissions import *


#https://www.bezkoder.com/django-rest-api/
# TODO: Fix DELETE, issue: ForeignKey delete policy
class coursePk(APIView):
    permission_classes = [isNormalUser |isAdminUser | isSuperUser]
    serializer_class = CourseSerializer
    Model = Course
    queryset = Model.objects.all()

    """
    Get course by pk
    """
    def get(self, request, pk):
        try:
            instance = self.queryset.get(pk=pk)
        except self.Model.DoesNotExist:
            return JsonResponse({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        serializer = self.serializer_class(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    """
    Delete course if user is admin or superuser
    """
    def delete(self, request, pk):
        print("entering delete")
        if isNormalUser():
            return JsonResponse({'detail': 'Normal user can not delete course'}, status=status.HTTP_403_FORBIDDEN)
        try:
            instance = self.queryset.get(pk=pk)
        except Course.DoesNotExist:
            return JsonResponse({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        instance.delete()
        return JsonResponse({'detail': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    """
    Update course if user is admin or superuser
    """
    def put(self, request, pk):
        if isNormalUser():
            return JsonResponse({'detail': 'Normal user can not update course'}, status=status.HTTP_403_FORBIDDEN)
        try:
            instance = self.queryset.get(pk=pk)
        except self.Model.DoesNotExist:
            return JsonResponse({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        instance_data = JSONParser().parse(request)
        serializer = self.serializer_class(instance, data=instance_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class coursesByUni(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = CourseSerializer
    Model = Course
    queryset = Model.objects.all()

    """
    Get list of courses by university if normaluser else get all courses
    """
    def get(self, request, uni):
        user = get_user(request)

        try:
            uni = University.objects.get_by_natural_key(uni)
        except University.DoesNotExist:
            return JsonResponse({'detail': 'The university does not exist'}, status=status.HTTP_404_NOT_FOUND)

        instances = uni.courses.all()
        serializer = self.serializer_class(instances, many=True)
        return JsonResponse(serializer.data, safe=False)

    """
    Post course by uni if user is admin or superuser. if uni doesn't exist, create it.
    """
    def post(self, request, uni):
        user = get_user(request)
        if not (user.is_superuser or user.is_admin):
            return JsonResponse({'detail': 'Normal user can not post course'}, status=status.HTTP_403_FORBIDDEN)

        instance_data = JSONParser().parse(request)
        try:
            uni = University.objects.get(university_name=uni)
        except University.DoesNotExist:
            uni = University.objects.create(university_name=uni)

        instance_data['university'] = uni.pk
        serializer = self.serializer_class(data=instance_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
