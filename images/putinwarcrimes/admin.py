from django.contrib import admin
from .models import Language, Photo, Category, PhotoDescription, Categorydescription


@admin.register(Language)
class LangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default')
    list_filter = ('name',)
    search_fields = ('name', )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created', 'updated', 'category_id')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(PhotoDescription)
class PhotoDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'photo_id', 'language_id')
    search_fields = ('id', 'name', 'language_id')


@admin.register(Categorydescription)
class CategorydescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('id', 'name', 'language_id', 'category_id')
