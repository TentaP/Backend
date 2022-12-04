from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tentap.serializers import CommentSerializer
from tentap.models import Comment, Review, File, Course 
from tentap.permissions import *

"""
api/file/<int:pk>/comments
"""
class CommentListByFile(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    queryset = File.objects
    serializer_class = CommentSerializer

    """
    Get list of comments by file
    """
    def get(self, request, pk):
        try:
            file = queryset.get(pk=pk)
            comments = file.comments.all()
            serializer = serializer_class(comments, many=True)
            return Response(serializer.data)
        except  File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
api/comment/<int:pk>
"""
class Comment(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    queryset = Comment.objects
    serializer_class = CommentSerializer

    """
    Get specific comment
    """
    def get(self, request, pk):
        try:
            comment = queryset.get(pk=pk)
            serializer = serializer_class(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Edit comment if normaluser is the author of the comment
    Admin and Superuser can not edit any comment
    """
    def put(self, request, pk):
        try:
            comment = queryset.get(pk=pk)
            serializer = serializer_class(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Delete comment if normaluser is the author of the comment
    if admin or superuser, delete comment
    """
    def delete(self, request, pk):
        try:
            user = get_user(request)
            comment = queryset.get(pk=pk)
            if isNormalUser:
                if user == comment.author:
                    comment.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
