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
from tentap.models import Course
from tentap.permissions import *


#https://www.bezkoder.com/django-rest-api/
# TODO: Fix DELETE, issue: ForeignKey delete policy
@api_view(['GET', 'DELETE'])
def course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'message': 'The course does not exist'}, status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        course_serializer = CourseSerializer(course)
        return JsonResponse(course_serializer.data)
    
    elif request.method == 'DELETE':
        course.delete()
        return JsonResponse({'message': 'Course was deleted successfully!'}, status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def courses(request):
    courses = Course.objects.all()
    if request.method == 'GET':
        course_serializer = CourseSerializer(courses, many=True)
        return JsonResponse(course_serializer.data, safe=False)

    elif request.method == 'POST':
        permission_classes = [isNormalUser | isAdminUser | isSuperUser]
        token = request.COOKIES.get('jwt')
        print(token)

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
            return JsonResponse(status.HTTP_403_FORBIDDEN)

        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse(course_serializer.data, status.HTTP_201_CREATED) 
        return JsonResponse(course_serializer.errors, status.HTTP_400_BAD_REQUEST)





