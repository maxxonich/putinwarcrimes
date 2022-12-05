from django.db import models


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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default="1")

    class Meta:
        db_table = 'category'
        verbose_name_plural = "Categories"


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=1000)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, null=True)
    updated = models.DateField(auto_now=True, null=True)

    class Meta:
        db_table = 'photo'
        verbose_name_plural = "Photos"


class PhotoDescription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE)
    size = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'photo_description'
        verbose_name_plural = "Photos descriptions"


class Categorydescription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    language_id = models.ForeignKey(Language, null=True, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category_description'
        verbose_name_plural = "Categories descriptions"


class Genocide(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    latest = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'genocide'
        verbose_name_plural = "Genocides"


class GenocideDescription(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    language_id = models.ForeignKey(Language, null=True, on_delete=models.CASCADE)
    genocide_id = models.ForeignKey(Genocide, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'genocide_desc'
        verbose_name_plural = "Genocide descriptions"
