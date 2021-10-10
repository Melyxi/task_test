from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


class MyUserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50, verbose_name="username")
    full_name = models.CharField(max_length=500, verbose_name="Полное имя")
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.full_name}"


class Tasks(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название задачи", unique=True)
    description = models.TextField(verbose_name="Описание задачи", blank=True)
    end_date = models.DateTimeField(verbose_name="Дата завершения")
    users = models.ManyToManyField(MyUserModel)
