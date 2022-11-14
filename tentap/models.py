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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class File(models.Model):
    # Types of files, subject to change.
    class fileType(models.TextChoices):
        EX = 'EX', 'Exam'
        AS = 'AS', 'ASSIGNMENT'
        LB = 'LB', 'Lab'

    file_name = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    at_university = models.ForeignKey('University', on_delete=models.CASCADE)    
    date_of_uploading = models.DateTimeField(auto_now=True)
    reviews = models.ForeignKey('Review', related_name='reviews', on_delete=models.CASCADE)
    file_type = models.CharField(
        max_length=2,
        choices=fileType.choices,
        default=fileType.AS
    )

class University(models.Model):
    university_name = models.CharField(max_length=200,unique=True)
    courses = models.ForeignKey('Course', related_name='Courses', on_delete=models.CASCADE)

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    at_university = models.ForeignKey('University', on_delete=models.CASCADE) 
    Files = models.ForeignKey('File', related_name='files', on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey('User',related_name='Author', on_delete=models.CASCADE)
    review = models.DecimalField(decimal_places=1, max_digits=1)
    body = models.CharField(max_length=700)

