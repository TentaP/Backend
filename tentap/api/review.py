from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from tentap.serializers import ReviewSerializer
from tentap.models import Review, File, Course 
from tentap.permissions import *

"""
Get list of reviews by course
api/course/<int:pk>/reviews
"""
class ReviewListByCourse(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = ReviewSerializer
    Model = Course
    objects = Model.objects.all()

    def get(self, request, pk):
        try:
            model = self.objects.get(pk=pk)
        except self.Model.DoesNotExist:
            return Response({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        reviews = model.Reviews.all()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)

"""
Get list of reviews by course
api/file/<int:pk>/reviews
"""
class ReviewListByFile(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = ReviewSerializer
    Model = File
    objects = Model.objects.all()

    def get(self, request, pk):
        try:
            model = self.objects.get(pk=pk)
        except self.Model.DoesNotExist:
            return Response({'detail': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        reviews = model.Reviews.all()
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)

"""
api/review/course/<int:course_pk>
api/review/file/<int:file_pk>
"""
class ReviewItem(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = ReviewSerializer
    Model = Review
    queryset = Model.objects.all()

    """
    Post review to Course or File
    A user can only post one review to a course or file
    """
    def post(self, request, course_pk=None, file_pk=None):
        if course_pk and file_pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            data = JSONParser().parse(request)
        except:
            return Response({'detail': 'malformed request'},status=status.HTTP_400_BAD_REQUEST)
        user = get_user(request)

        if course_pk:
            if user.Reviews.filter(course=course_pk).exists():
                return Response({'detail': 'You have already reviewed this course'}, status=status.HTTP_400_BAD_REQUEST)
            data['course'] = course_pk
        else:
            if user.Reviews.filter(file=file_pk).exists():
                return Response({'detail': 'You have already reviewed this file'}, status=status.HTTP_400_BAD_REQUEST)
            data['file'] = file_pk

        data['author'] = user.pk

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, course_pk=None, file_pk=None):
        if course_pk and file_pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if course_pk:
            try:
                reviews = self.queryset.filter(course=course_pk)
            except self.Model.DoesNotExist:
                return Response({'detail': 'The course does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                reviews = self.queryset.filter(file=file_pk)
            except self.Model.DoesNotExist:
                return Response({'detail': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, course_pk = None, file_pk = None):
        if course_pk and file_pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_user(request)
        if course_pk:
            try:
                review = self.queryset.get(course=course_pk, author=user.pk)
            except self.Model.DoesNotExist:
                return Response({'detail': 'The review does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                review = self.queryset.get(file=file_pk, author=user.pk)
            except self.Model.DoesNotExist:
                return Response({'detail': 'The review does not exist'}, status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewPk(APIView):
    permission_classes = [isNormalUser | isAdminUser | isSuperUser]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    """
    Get specific review
    """
    def get(self, request, pk):
        print("review pk get "+ str(pk))
        try:
            review = self.queryset.get(pk=pk)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(review)
        return Response(serializer.data)

    """
    Edit review if normaluser is the author of the review
    Admin and Superuser can not edit any review
    """
    def put(self, request, pk):
        user = get_user(request)
        try:
            review = self.queryset.get(pk=pk)
            if isNormalUser and review.author != user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            review.body = request.data['body']
            review.review = request.data['review']
            review.save()
            serializer = self.serializer_class(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Delete review if normaluser is the author of the review
    if admin or superuser, delete review
    """
    def delete(self, request, pk):
        user = get_user(request)
        try:
            review = self.queryset.get(pk=pk)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if isNormalUser and review.author != user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
