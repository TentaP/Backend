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

from tentap.serializers import UsersSerializer, UniversitySerializer
from tentap.models import University
from tentap.permissions import *


#https://www.bezkoder.com/django-rest-api/
# TODO: Fix DELETE, issue: ForeignKey delete policy
class universitypk(APIView):
    permission_classes = [isAdminUser | isSuperUser]
    def get(request, pk):
        university_serializer = UniversitySerializer(university)
        return JsonResponse(university_serializer.data)
        
    def delete(request, pk):
        university.delete()
        return JsonResponse({'message': 'University was deleted successfully!'}, status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def university(request):
    universitys = University.objects.all()
    if request.method == 'GET':
        university_serializer = UniversitySerializer(universitys, many=True)
        return JsonResponse(university_serializer.data, safe=False)

    elif request.method == 'POST':
        university_data = JSONParser().parse(request)
        university_serializer = UniversitySerializer(data=university_data)
        if university_serializer.is_valid():
            university_serializer.save()
            return JsonResponse(university_serializer.data, status.HTTP_201_CREATED) 
        return JsonResponse(university_serializer.errors, status.HTTP_400_BAD_REQUEST)





