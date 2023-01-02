from datetime import datetime, timedelta

import jwt
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import *
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from tentap.models import University, ActivationLink, PasswordResetToken
from tentap.serializers import UsersSerializer, ActivationLinkSerializer, PasswordResetTokenSerializer
from tentap.permissions import *
from tentap.security import email_validation, get_random_hash
from django.core.mail import send_mail

class usersList(APIView):
    permission_classes = [isAdminUser | isSuperUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return JsonResponse(serializer.data, status=200,safe=False)

class userDetails(APIView):
    permission_classes = [isAdminUser | isSuperUser]

    def get(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({"detail": e}, status=500)  #TODO
        serializer = UsersSerializer(user)
        return JsonResponse(serializer.data)

    def put(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            return Response({"detail": e}, status=500)  #TODO
        data = JSONParser().parse(request)
        serializer = UsersSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            return JsonResponse({"detail": e}, status=500)  # TODO
        user.delete()
        return JsonResponse({"detail":"successfully deleted"},status=204)


class userView(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def get(self, request):
        token = request.headers.get("Authorization")

        if not token:
            raise NotAuthenticated("not authenticated!")

        try:
            payload = jwt.decode(token, secret.SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise NotAuthenticated("not authenticated!")

        user = User.objects.filter(id=payload["user_id"]).first()
        serializer = UsersSerializer(user)
        return Response(serializer.data)

class userUni(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = UsersSerializer

    def put(self, request, pk):
        user = get_user(request)
        try:
            university = University.objects.get(pk=pk)
        except University.DoesNotExist:
            return Response({"detail": "University does not exist"}, status=404)

        user.university = university
        user.save()
        return Response({"detail": "successfully updated"}, status=200)

