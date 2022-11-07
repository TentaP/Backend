from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


# class User(models.Model):
#     user_name = models.CharField(max_length=200, unique=True)
#     e_mail = models.EmailField(unique=True)
#     password = models.CharField(max_length=200)
#     is_admin = models.BooleanField(default=False)
#     is_super_user = models.BooleanField(default=False)
#     # university_name = models.CharField(max_length=200) TODO


# Files model skeleton
"""
class Files(models.Model):
    file_name = models.CharField(max_length=200)
    uploaded_by = Users.user_name  # change to be related to the user
    course_name = models.CharField(max_length=200)
    university_name = models.CharField(max_length=200)  # change to be related to the university
    date_of_uploading = models.DateTimeField(auto_now=True)
"""

# University model skeleton
"""
class University(models.Model):
    university_name = models.CharField(max_length=200,unique=True)
    courses = ArrayField(
        models.CharField(max_length=200)
    )
"""

# Courses model skeleton
"""
class Courses(models.Model):
    course_name = models.CharField(max_length=200)
    at_university = models.CharField(max_length=200) # TODO change to be related to university model
    Files = models.CharField(max_length=200) # TODO change to be related to files model 
"""
