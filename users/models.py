from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from word.models import Word


# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(null=True, blank=True, max_length=155, verbose_name='نام')
    last_name = models.CharField(null=True, blank=True, max_length=155, verbose_name='نام خانوادگی')
    username = models.CharField(max_length=15, unique=True, verbose_name="شماره موبایل")
    is_vip = models.BooleanField(default=False, verbose_name="نوع کاربر")
    picture = models.ImageField(null=True, blank=True, upload_to="images", verbose_name="عکس پروفایل")

    def is_valid_iranian_mobile(self):
        pattern = r'^09[0-9]{9}$'
        return re.match(pattern, self.username)

    def clean(self):
        super().clean()
        if not self.is_valid_iranian_mobile():
            raise ValidationError({'username': 'شماره موبایل وارد شده معتبر نمی‌باشد.'})

    def __str__(self):
        return str(self.first_name) + str(self.last_name)


class Interest(models.Model):
    word = models.ManyToManyField(Word, verbose_name='کلمه', related_name='user')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='favorite')
