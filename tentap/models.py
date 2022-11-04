from django.db import models


class Users(models.Model):
    user_name = models.CharField(max_length=200, unique=True)
    e_mail = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)



