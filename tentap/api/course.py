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

from tentap.serializers import UsersSerializer, CourseSerializer, UniversitySerializer
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


class courses(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    """
    Get list of courses by university if normal user else get all courses
    """
    def get(self, request):
        user = get_user(request)
        if not user:
            return Response({"detail": ""}, status=500)  # TODO

        if user.is_admin or user.is_admin:
            instances = Course.objects.all()

        else:
            instances = Course.objects.filter(university=user.university).all()

        serializer = CourseSerializer(instances, many=True)
        return JsonResponse(serializer.data, safe=False)

    """
    Post course if user is admin or superuser
    """
    def post(self, request):
        user = get_user(request)
        instance_data= JSONParser().parse(request)
        try:
            university = University.objects.get(university_name = instance_data['university'])
        except:
            university = None

        if not user:
            return Response({"detail": ""}, status=500)  # TODO

        if user.is_admin or user.is_admin:
            if university is None:
                payload = {"university_name":str(instance_data['university'])}
                university_serializer = UniversitySerializer(data=payload)
                university_serializer.is_valid(raise_exception=True)
                university_serializer.save()
                university = University.objects.get(university_name=instance_data['university'])
                instance_data['university'] = university.id
                course_serializer = CourseSerializer(data=instance_data)
                course_serializer.is_valid(raise_exception=True)
                course_serializer.save()
                return JsonResponse(course_serializer.data,status=201)
            else:
                instance_data['university'] = university.id
                course_serializer = CourseSerializer(data=instance_data)
                course_serializer.is_valid(raise_exception=True)
                course_serializer.save()
                return JsonResponse(course_serializer.data,status=201)

        else:
            return JsonResponse({'detail': 'Normal user cannot post course'}, status=status.HTTP_403_FORBIDDEN)


