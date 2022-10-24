from django.contrib import admin
from .models import Language, Photo


@admin.register(Language)
class LangAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default')
    list_filter = ('name',)
    search_fields = ('name', )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name','pub_date',)