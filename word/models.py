

# Create your models here.
from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    slug = models.CharField(max_length=255, verbose_name='اسلاگ')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='والدین', related_name='children',null=True,blank=True)

    def __str__(self):
        return self.title


class Word(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    video = models.FileField(upload_to='film', verbose_name='فیلم')
    pronunciation = models.CharField(max_length=50, verbose_name='تلفظ')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    slug = models.CharField(max_length=255, verbose_name='اسلاگ')

    def __str__(self):
        return self.title
