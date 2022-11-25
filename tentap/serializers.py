from rest_framework import serializers
from django.forms import ModelForm
from tentap.models import User, Course, File, University


# https://www.django-rest-framework.org/tutorial/1-serialization/

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin', 'is_superuser', 'is_active']
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
        fields = ['course_name', 'university', 'description']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.university = validated_data.get('university', instance.university)
        instance.description = validated_data.get('description', instance.description)
        return instance

# File
class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file',  'course', 'at_university', 'file_type']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file',  'course', 'at_university', 'date_of_uploading', 'reviews', 'file_type']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file_name = validated_data.get('file_name', instance.file_name)
        instance.file = validated_data.get('file', instance.file)
        instance.image = validated_data.get('image', instance.image)
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

