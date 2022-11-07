import datetime
import jwt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from tentap.serializers import UsersSerializer
from tentap.permissions import *


class signup(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UsersSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"RESPONSE": "CREATED"}, status=201)


class login(APIView):

    def post(self, request):
        login_using_user_name = False
        data = JSONParser().parse(request)
        if list(data.keys()) == ['username', 'password']:
            login_using_user_name = True
        elif list(data.keys()) == ['email', 'password']:
            login_using_user_name = False

        user = None
        password = data['password']
        if login_using_user_name:
            username = data['username']
            user = User.objects.filter(username=username).first()
        elif not login_using_user_name:
            email = data['email']
            user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, secret.SECRET_KEY, algorithm='HS256')

        res = Response()
        res.set_cookie(key='jwt', value=token, httponly=True)
        res.data = {
            'jwt': token
        }
        return res


class logout(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        res = Response()
        res.delete_cookie('jwt')
        res.data = {
            'message': 'success'
        }
        return res


class userView(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, secret.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UsersSerializer(user)
        return Response(serializer.data)


@csrf_exempt
def users_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['password'] = encode_password(data['password'])
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"TEST": "DDF"}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_details(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.objects.get(pk=pk).DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UsersSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
