from rest_framework import serializers
from django.forms import ModelForm
from tentap.models import User, Course, File, University, ActivationLink, PasswordResetToken, Review, Comment


# https://www.django-rest-framework.org/tutorial/1-serialization/

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','university', 'password', 'is_admin', 'is_superuser', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        print(password)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        print(password)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


# Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'university', 'description']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.university = validated_data.get('university', instance.university)
        instance.description = validated_data.get('description', instance.description)
        return instance


# File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['filename', 'uploaded_by', 'file', 'course', 'at_university', 'date_of_uploading', 'file_type']

    def create(self, validated_data):
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.filename = validated_data.get('filename', instance.filename)
        instance.file_type = validated_data.get('file_type', instance.file)
        return instance


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'university_name']

    def create(self, validated_data):
        return University.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.university_name = validated_data.get('university_name', instance.university_name)
        return instance


class ActivationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationLink
        fields = ['user', 'expiry_data', 'hash']

    def create(self, validated_data):
        return ActivationLink.objects.create(**validated_data)


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = ['user', 'expiry_data', 'hash']

    def create(self, validated_data):
        return PasswordResetToken.objects.create(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'author', 'review', 'body', 'course', 'file']

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.review = validated_data.get('review', instance.review)
        instance.body = validated_data.get('body', instance.body)
        return instance

"""
TODO: edited comment has a edited date
"""
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'comment', 'file']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        return instance

