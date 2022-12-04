from datetime import datetime, timedelta

import jwt
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import *
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from tentap.models import ActivationLink, PasswordResetToken
from tentap.serializers import UsersSerializer, ActivationLinkSerializer, PasswordResetTokenSerializer
from tentap.permissions import *
from tentap.security import email_validation, get_random_hash
from django.core.mail import send_mail


# https://www.youtube.com/watch?v=PUzgZrS_piQ&ab_channel=ScalableScripts
# https://www.youtube.com/watch?v=yiYpFMk9QdA&t=355s&ab_channel=PrettyPrinted
# https://www.django-rest-framework.org/api-guide/exceptions/#parseerror list of exceptions that we can use
class signup(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        payload = {
            "username": str(data["username"]).lower(),
            "email": str(data["email"]).lower(),
            "password": data["password"]
        }
        if not email_validation(data['email']):
            raise NotAcceptable("wrong email format")

        user_serializer = UsersSerializer(data=payload)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        hash_ = get_random_hash()
        msg = f"http://127.0.0.1:8000/api/verifection/{user_serializer.data['email']}/{hash_}"
        activation_link_payload = {
            "user": user_serializer.data['id'],
            "hash": hash_,
            "expiry_data": timezone.now() + timedelta(minutes=3)  # TODO change this (hours=24)
        }
        activationLink_serializer = ActivationLinkSerializer(data=activation_link_payload)
        activationLink_serializer.is_valid(raise_exception=True)
        activationLink_serializer.save()
        send_mail("verify your email", msg, "noubah-8@studnet.ltu.se", [str(user_serializer.data["email"])])
        print(msg)  # TODO remove this
        return Response({"detail": "account created successfully"}, status=201)


class login(APIView):

    def post(self, request):
        data = JSONParser().parse(request)

        if list(data.keys()) == ["username", "password"]:
            login_using_user_name = True
        elif list(data.keys()) == ["email", "password"]:
            login_using_user_name = False
        else:
            raise NotAcceptable("wrong entry, insert email or username")

        user = None
        password = data["password"]
        if login_using_user_name:
            username = str(data["username"]).lower()
            user = User.objects.filter(username=username).first()
        elif not login_using_user_name:
            email = str(data["email"]).lower()
            user = User.objects.filter(email=email).first()

        if user is None:
            raise NotFound("user not found!")

        if not user.is_active:
            raise MethodNotAllowed("your account is not active!")

        if not user.check_password(password):
            raise NotAcceptable("incorrect password!")

        refresh = RefreshToken.for_user(user)

        resp = Response()
        resp.data = {
            'detail': "successfully logged in",
            'access': str(refresh.access_token),
        }
        resp.status_code = 200
        print(jwt.decode(str(refresh.access_token), secret.SECRET_KEY, algorithms='HS256'))
        return resp


class logout(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def post(self, request):
        token = request.headers.get("Authorization")[7:]
        if not token:
            raise NotAuthenticated("not authenticated!")
        resp = Response()
        resp.delete_cookie('jwt')
        resp.data = {
            "detail": "successfully logged out"
        }
        resp.status_code = 200
        return resp


# TODO move this to a new view
class userView(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def get(self, request):
        token = request.headers.get("Authorization")[7:]

        if not token:
            raise NotAuthenticated("not authenticated!")

        try:
            payload = jwt.decode(token, secret.SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise NotAuthenticated("not authenticated!")

        user = User.objects.filter(id=payload["user_id"]).first()
        serializer = UsersSerializer(user)
        return Response(serializer.data)


class emailVerification(APIView):
    def get(self, request, email: str, hash_: str):
        user = User.objects.filter(email=email.lower()).first()
        if not user:
            return Response({"detail": ""}, status=500)  # TODO

        if user.is_active:
            return Response({"detail": "account is already active!"}, status=500)

        activation_link = ActivationLink.objects.filter(user_id=user.id).first()
        if hash_ == activation_link.hash and timezone.now() <= activation_link.expiry_data:
            user.is_active = True
            user.save()
            activation_link.delete()
            return Response({"detail": "account activated!"}, status=200)
        elif hash_ != activation_link.hash:
            return Response({"detail": "wrong activation link!"}, status=500)
        elif timezone.now() > activation_link.expiry_data:
            return Response({"detail": "activation link is expired!"}, status=500)


class setSuperUser(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data['username']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise NotFound('user not found!')
        if user.is_superuser:
            raise NotAcceptable(f"{username} is already a super_user")
        user.is_superuser = True
        user.is_admin = True
        try:
            user.save()
        except Exception:
            raise {
                "status_code": 500,
                "detail": "an error occurred while saving in the database "
            }

        return Response({"detail": f"{username} is superuser now!"}, status=201)


class setAdmin(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data["username"]
        user = User.objects.filter(username=username).first()
        if user is None:
            raise NotFound("user not found!")
        if user.is_admin:
            raise NotAcceptable(f"{username} is already an admin")
        user.is_admin = True
        try:
            user.save()
        except Exception:
            raise {
                "status_code": 500,
                "detail": "An Error occurred while saving in the database"
            }
        return Response({"detail": f"{username} is admin now!"}, status=201)


class removeAdmin(APIView):
    permission_classes = [isSuperUser]

    def put(self, request):
        data = JSONParser().parse(request)
        username = data["username"]
        user = User.objects.filter(username=username).first()
        if user is None:
            raise NotFound("user not found!")
        if not user.is_admin:
            raise NotAcceptable(f"{username} is not an admin")
        user.is_admin = False
        try:
            user.save()
        except Exception:
            raise {
                "status_code": 500,
                "detail": "an error occurred while saving in the database "
            }
        return Response({"detail": f"{username} is removed as an admin now!"}, status=200)


class requestPasswordResetToken(APIView):

    def post(self, request):
        data = JSONParser().parse(request)
        email = data["email"]
        user = User.objects.filter(email=email).first()

        if user is None:
            raise NotFound("user not found!")

        # update the hash if it is already in the db
        passwordResetToken = PasswordResetToken.objects.filter(user_id=user.id).first()
        hash_ = get_random_hash()
        if passwordResetToken:
            passwordResetToken.delete()
            passwordResetToken.save()

        password_reset_link_payload = {
            "user": user.id,
            "hash": str(hash_),
            "expiry_data": timezone.now() + timedelta(minutes=60)  # TODO change this (hours=24)
        }
        password_reset_link_serializer = PasswordResetTokenSerializer(data=password_reset_link_payload)
        password_reset_link_serializer.is_valid(raise_exception=True)
        password_reset_link_serializer.save()
        send_mail("reset your password with this token", str(hash_), "noubah-8@studnet.ltu.se", [str(email)])
        print(hash_)

        return Response({"detail": f"an email has been sent to {email}"}, status=200)


class resetPasswordViaToken(APIView):
    def put(self, request):
        data = JSONParser().parse(request)
        email = data["email"]
        token = data["token"]
        password = data["password"]

        user = User.objects.filter(email=email.lower()).first()
        if not user:
            return Response({"detail": "email not found!"}, status=500)  # TODO

        reset_token = PasswordResetToken.objects.filter(user_id=user.id).first()
        if not reset_token:
            return Response({"detail": "Token not found!"}, status=500)  # TODO

        if token == reset_token.hash and timezone.now() <= reset_token.expiry_data:
            user.set_password(password)
            user.save()
            reset_token.delete()
            return Response({"detail": f"password for {email} has been updated"}, status=201)

        elif token != reset_token.hash:
            return Response({"detail": "wrong reset token!"}, status=500)
        elif timezone.now() > reset_token.expiry_data:
            print(timezone.now())
            print(reset_token.expiry_data)
            return Response({"detail": "reset token is expired!"}, status=500)


class resetPassword(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]

    def put(self, request):
        token = request.headers.get("Authorization")[7:]

        if not token:
            raise NotAuthenticated('not authenticated!')

        try:
            payload = jwt.decode(token, secret.SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('session expired!')

        user = User.objects.filter(id=payload["user_id"]).first()
        try:
            data = JSONParser().parse(request)
            newPassword = data["password"]
        except Exception:
            raise ParseError("incorrect json entry!")
        user.set_password(newPassword)
        try:
            user.save()
        except Exception:
            raise {
                "status_code": 500,
                "detail": "an error occurred while saving in the database "
            }
        return Response({"detail": f"password for {user.email} has been updated"}, status=201)


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
