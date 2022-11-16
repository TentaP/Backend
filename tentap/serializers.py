from rest_framework import serializers
from tentap.models import User, Course, File, University


# https://www.django-rest-framework.org/tutorial/1-serialization/

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin', 'is_superuser']
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

"""
class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = ['id', 'user_name', 'access_token', 'refresh_token']

    def create(self, validated_data):
        return Tokens.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.access_token = validated_data.get('access_token', instance.access_token)
        instance.refresh_token = validated_data.get('refresh_token', instance.refresh_token)
        instance.save()
        return instance
"""

# Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'at_university', 'files']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.at_university = validated_data.get('at_university', instance.at_university)
        instance.files = validated_data.get('files', instance.files)
        return instance

# File
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'uploaded_by', 'File', 'course', 'at_university', 'date_of_uploading', 'reviews', 'file_type']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file_name = validated_data.get('file_name', instance.file_name)
        instance.file = validated_data.get('file', instance.file)
        return instance

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['university_name']

    def create(self, validated_data):
        return University.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.university_name = validated_data.get('university_name', instance.university_name)
        return instance

