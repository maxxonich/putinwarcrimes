from django.db import models
import os

# from django.contrib.auth.models import User
# from django.utils import timezone


class Photo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='files/front/upload/', height_field=None,
                              width_field=None, max_length=100)
    description = models.TextField

    class Meta:
        verbose_name_plural = "Photos"

    def __str__(self):
        return self.name


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    default = models.BooleanField(default=False)

    class Meta:
        db_table = 'language'
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=255)
    description = models.TextField
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    # file_name = models.ForeignKey(Photo, on_delete=models.CASCADE)
    # file_stats = models.IntegerField(os.stat(file_name))
    def __str__(self):
        return self.name

    class Meta:

        db_table = 'category'
        verbose_name_plural = "Categories"

