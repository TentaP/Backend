from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tentap.serializers import ReviewSerializer
from tentap.models import Review, File, Course 
from tentap.permissions import *

"""
api/course/<int:pk>/reviews
"""
class ReviewListByCourse(APIView):
    permission_classes = [isNormalUser, isAdminUser, isSuperUser]

    """
    Get list of reviews by course
    """
    def get(self, request):
        course = Course.objects.get_by_natural_key(request.GET.get('course_name'), request.GET.get('university'))
        reviews = course.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

"""
api/file/<int:pk>/reviews
"""
class ReviewListByFile(APIView):
    permission_classes = [isNormalUser, isAdminUser, isSuperUser]

    """
    Get list of reviews by file
    """
    def get(self, request, pk):
        file = File.objects.get(pk=pk)
        reviews = file.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
"""
api/review/<int:pk>
"""
class Review(APIView):
    permission_classes = [isNormalUser, isAdminUser, isSuperUser]

    """
    Post review to Course or File
    """
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    Get specific review
    """
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Edit review if normaluser is the author of the review
    Admin and Superuser can not edit any review
    """
    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data)
            if isNormalUser and review.author != request.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Delete review if normaluser is the author of the review
    if admin or superuser, delete review
    """
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
