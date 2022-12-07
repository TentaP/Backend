from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from tentap.managers import CourseManager, UniversityManager

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.uploaded_by.id, filename)

class File(models.Model):
    # Types of files, subject to change.
    filename = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey('User', related_name="Files", on_delete=models.PROTECT)

    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    course = models.ForeignKey('Course', related_name="Files", on_delete=models.PROTECT)
    at_university = models.ForeignKey('University', related_name="Files", on_delete=models.PROTECT)
    date_of_uploading = models.DateTimeField(auto_now=True)

    comments = models.ForeignKey('Comment', related_name='File', on_delete=models.CASCADE, blank=True, null=True)
    has_solutions = models.BooleanField(default=False)

    class fileType(models.TextChoices):
        EX = 'EX', 'Exam'
        AS = 'AS', 'Assignment'
        LB = 'LB', 'Lab'

    file_type = models.CharField(
        max_length=2,
        choices=fileType.choices,
        default=fileType.AS
    )


class University(models.Model):
    university_name = models.CharField(max_length=200, unique=True)

    objects = UniversityManager()

    def natural_key(self):
        return (self.university_name)



class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)
    university = models.ForeignKey(University, related_name='courses', on_delete=models.PROTECT)
    description = models.CharField(max_length=700)

    objects = CourseManager()

    class Meta:
        unique_together = ('course_name', 'university')


class Comment(models.Model):
    author = models.ForeignKey('User', related_name='Comments', on_delete=models.PROTECT)
    file = models.ForeignKey('File', related_name='Comments', on_delete=models.PROTECT, blank=True, null=True)

    comment = models.CharField(max_length=700)


class Review(models.Model):
    author = models.ForeignKey('User', related_name='Reviews', on_delete=models.PROTECT)
    course = models.ForeignKey('Course', related_name='Reviews', on_delete=models.PROTECT, blank=True, null=True)
    file = models.ForeignKey('File', related_name='Reviews', on_delete=models.PROTECT, blank=True, null=True)

    review = models.DecimalField(decimal_places=1, max_digits=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    body = models.CharField(max_length=700)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    university = models.ForeignKey(University, related_name="Users", null=True, blank=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class ActivationLink(models.Model):
    user = models.ForeignKey('User', related_name='ActivationLink', on_delete=models.PROTECT)
    expiry_data = models.DateTimeField(null=True)
    hash = models.CharField(max_length=256)


class PasswordResetToken(models.Model):
    user = models.ForeignKey('User', related_name='PasswordResetLink', on_delete=models.PROTECT)
    expiry_data = models.DateTimeField(null=True)
    hash = models.CharField(max_length=256)

