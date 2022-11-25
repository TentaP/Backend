from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


# Create your models here.

class File(models.Model):
    # Types of files, subject to change.
    file_name = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey('User', related_name="Files",  on_delete=models.PROTECT)

    file = models.FileField(upload_to='documents/', blank=True, null=True)

    course = models.ForeignKey('Course', related_name="Files", on_delete=models.PROTECT)
    at_university = models.ForeignKey('University', related_name="Files", on_delete=models.PROTECT)    
    date_of_uploading = models.DateTimeField(auto_now=True)
    reviews = models.ForeignKey('Review', related_name='File', on_delete=models.CASCADE, blank=True, null=True)

    class fileType(models.TextChoices):
        EX = 'EX', 'Exam'
        AS = 'AS', 'ASSIGNMENT'
        LB = 'LB', 'Lab'
    file_type = models.CharField(
        max_length=2,
        choices=fileType.choices,
        default=fileType.AS
    )

class University(models.Model):
    university_name = models.CharField(max_length=200,unique=True)

class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)
    university = models.ForeignKey(University, related_name='Courses', on_delete=models.PROTECT)
    description = models.CharField(max_length=700)

class Comment(models.Model):
    comment = models.CharField(max_length=700)
    course = models.ForeignKey('File', related_name='Comments', on_delete=models.PROTECT)
    author = models.ForeignKey('User',related_name='Comments', on_delete=models.PROTECT)

class Review(models.Model):
    author = models.ForeignKey('User',related_name='Reviews', on_delete=models.PROTECT)
    review = models.DecimalField(decimal_places=1, max_digits=1)
    body = models.CharField(max_length=700)

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    university = models.ForeignKey(University, related_name="Users", null=True, blank=True,  on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
