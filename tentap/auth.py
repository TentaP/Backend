import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from tentap.serializers import UsersSerializer
from tentap.permissions import *
from tentap.security import encode_link, email_validation
from django.core.mail import BadHeaderError, send_mail


# https://www.youtube.com/watch?v=PUzgZrS_piQ&ab_channel=ScalableScripts
# https://www.youtube.com/watch?v=yiYpFMk9QdA&t=355s&ab_channel=PrettyPrinted
class signup(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        payload = {
            'username': str(data['username']).lower(),
            'email': str(data['email']).lower(),
            'password': data['password']
        }
        if not email_validation(data['email']):
            raise AuthenticationFailed('Wrong email format!')
        serializer = UsersSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        hash_ = serializer.data['email'] + secret.SECRET_KEY
        msg = f"http://127.0.0.1:8000/api/verifection/{serializer.data['email']}/{encode_link(hash_)}"
        send_mail('verify your email', msg, 'noubah-8@studnet.ltu.se', [str(serializer.data['email'])])
        print(f"http://127.0.0.1:8000/api/verifection/{serializer.data['email']}/{encode_link(hash_)}")  # SEND THIS
        # VIA EMAIL
        return JsonResponse({"RESPONSE": "CREATED"}, status=201)


class login(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        if list(data.keys()) == ['username', 'password']:
            login_using_user_name = True
        elif list(data.keys()) == ['email', 'password']:
            login_using_user_name = False
        else:
            raise AuthenticationFailed('Wrong input')

        user = None
        password = data['password']
        if login_using_user_name:
            username = str(data['username']).lower()
            user = User.objects.filter(username=username).first()
        elif not login_using_user_name:
            email = str(data['email']).lower()
            user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found!')

        if not user.is_active:
            raise AuthenticationFailed('Your account is not active!')

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


class emailVerification(APIView):
    def get(self, request, email: str, hash_: str):
        salted_email = email.lower() + secret.SECRET_KEY
        if hash_ == encode_link(salted_email):
            user = User.objects.filter(email=email.lower()).first()
            if user.is_active:
                raise AuthenticationFailed('account is already active')
            user.is_active = True
            user.save()
            return Response({'message': 'account activated!'})
        else:
            return Response({'message': 'wrong activation link'})


class setSuperUser(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user not found!')
        if user.is_superuser:
            raise AuthenticationFailed(f'{username} is already a super user')
        user.is_superuser = True
        user.is_admin = True
        user.save()
        return Response({'message': f'{username} is superuser now!'})


class setAdmin(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user not found!')
        if user.is_admin:
            raise AuthenticationFailed(f'{username} is already an admin')
        user.is_admin = True
        user.save()
        return Response({'message': f'{username} is admin now!'})


class removeAdmin(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user not found!')
        if not user.is_admin:
            raise AuthenticationFailed(f'{username} is not an admin')
        user.is_admin = False
        user.save()
        return Response({'message': f'{username} is removed as an admin now!'})


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
