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
class course(APIView):
    permission_classes = [isNormalUser |isAdminUser | isSuperUser]
    print("test")

    """
    Get course by pk
    """
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return JsonResponse({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        course_serializer = CourseSerializer(course)
        return JsonResponse(course_serializer.data)

    """
    Delete course if user is admin or superuser
    """
    def delete(self, request, pk):
        if isNormalUser():
            return JsonResponse({'detail': 'Normal user can not delete course'}, status=status.HTTP_403_FORBIDDEN)
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return JsonResponse({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        course.delete()
        return JsonResponse({'detail': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class courses(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    """
    Get list of courses by university if normaluser else get all courses
    """
    def get(self, request):
        user = get_user(request)
        if isNormalUser():
            courses = Course.objects.filter(university=user.university)
        elif isAdminUser() or isSuperUser():
            courses = Course.objects.all()
        else:
            return JsonResponse(status=status.HTTP_403_FORBIDDEN)
        course_serializer = CourseSerializer(courses, many=True)
        return JsonResponse(course_serializer.data, safe=False)

    """
    Post course if user is admin or superuser
    """
    def post(self, request):
        if isNormalUser():
            return JsonResponse({'detail': 'Normal user can not post course'}, status=status.HTTP_403_FORBIDDEN)

        course_data = JSONParser().parse(request)
        course_serializer = CourseSerializer(data=course_data)

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, secret.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session Expired!')

        user = User.objects.filter(id=payload['id']).first()

        if (user.university != course_data.university):
            return JsonResponse(status=status.HTTP_403_FORBIDDEN)

        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse(course_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





