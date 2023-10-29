# Create your models here.


from django.db import models
from slugify import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    slug = models.CharField(max_length=255, unique=True, verbose_name='اسلاگ')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='والدین', related_name='children',
                               null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Word(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
    video = models.FileField(upload_to='film', verbose_name='فیلم')
    pronunciation = models.CharField(max_length=50, verbose_name='تلفظ')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.CharField(max_length=255, verbose_name='اسلاگ', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug, allow_unicode=True)
        super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کلمه'
        verbose_name_plural = 'کلمه ها'
