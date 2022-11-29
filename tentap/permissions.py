import jwt
from rest_framework import permissions

import secret
from tentap.models import User


def get_user(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token, secret.SECRET_KEY, algorithms='HS256')
    user = User.objects.filter(id=payload['id']).first()
    return user


class isNormalUser(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            print("isNormalUser")
            if (not get_user(request).is_admin) and (not get_user(request).is_superuser):
                return True
            return False
        except Exception as e:
            print(e)
            return False


class isAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if get_user(request).is_admin:
                return True
            return False
        except:
            return False


class isSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if get_user(request).is_superuser:
                return True
            return False
        except:
            return False
