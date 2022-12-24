from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
import base64

from tentap.models import User
from tentap.serializers import AvatarSerializer
from tentap.permissions import *


class avatar_upload(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AvatarSerializer

    def post(self, request):
        user = get_user(request)
        avatar_path = user.get_avatar_path()
        if "static/avatar.png" not in avatar_path:
            user.set_avatar_to_default()
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    get image base64 encoded
    """
    def get(self, request):
        user = get_user(request)
        avatar_path = user.get_avatar_path()
        print(avatar_path)
        try:
            with open(avatar_path, "rb") as avatar_file:
                avatar_data = base64.b64encode(avatar_file.read()).decode('utf-8')
        except FileNotFoundError as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(avatar_data, status=status.HTTP_200_OK, safe=False)

    """
    remove avatar and set to default image
    """
    def delete(self, request):
        user = get_user(request)
        avatar_path = user.get_avatar_path()
        if "static/avatar.png" in avatar_path:
            return JsonResponse({'detail': 'no avatar picture'}, status=status.HTTP_404_NOT_FOUND)
        user.set_avatar_to_default()
        return JsonResponse({'detail': 'avatar picture deleted'}, status=status.HTTP_200_OK)


class avatar_pk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AvatarSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        avatar_path = user.get_avatar_path()
        print(avatar_path)
        try:
            with open(avatar_path, "rb") as avatar_file:
                avatar_data = base64.b64encode(avatar_file.read()).decode('utf-8')
        except FileNotFoundError as e:
            return JsonResponse({'detail': e}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(avatar_data, status=status.HTTP_200_OK, safe=False)
