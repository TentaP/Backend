from django.db import models
from django.contrib.postgres.fields import ArrayField


class Users(models.Model):
    user_name = models.CharField(max_length=200, unique=True)
    e_mail = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)
    # university = models.ForeignKey(University)


# Files model skeleton
"""
class File(models.Model):
    file_name = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
  # change to be related to the user
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)  # change to be related to the university
    date_of_uploading = models.DateTimeField(auto_now=True)

# University model skeleton
class University(models.Model):
    university_name = models.CharField(max_length=200,unique=True)
    courses = models.ForeignKey(Course, related_name='Courses')

# Courses model skeleton
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    at_university = models.ForeignKey(University) # TODO change to be related to university model
    Files = models.ForeignKey(File, related_name='files')  # TODO change to be related to files model 

"""