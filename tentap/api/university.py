from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status

from tentap.serializers import UniversitySerializer
from tentap.models import University
from tentap.permissions import *


#https://www.bezkoder.com/django-rest-api/
# TODO: Fix DELETE, issue: ForeignKey delete policy
class universitypk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    Model = University
    queryset = Model.objects.all()
    serializer_class = UniversitySerializer

    def get(self, request, pk):
        try:
            instance = self.queryset.get(pk=pk)
        except self.Model.DoesNotExist:
            return JsonResponse({'detail': 'The university does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, pk):
        user = get_user(request)
        if user.is_superuser or user.is_admin:
            try:
                instance = self.queryset.get(pk=pk)
            except self.Model.DoesNotExist:
                return JsonResponse({'detail': 'The university does not exist'}, status=status.HTTP_404_NOT_FOUND)
            instance.delete()
            return JsonResponse({'detail': 'University was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'detail': 'Normal users can not delete universities'},status=status.HTTP_401_UNAUTHORIZED)



class university(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    Model = University
    queryset = Model.objects.all()
    serializer_class = UniversitySerializer

    def get(self, request):
        instances = self.queryset.all()
        serializer = self.serializer_class(instances, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user(request)
        data = JSONParser().parse(request)
        if user.is_superuser or user.is_admin:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({"detail":"University has been added successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'detail': 'Normal users can not post universities'},status=status.HTTP_401_UNAUTHORIZED)

