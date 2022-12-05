import os
from datetime import datetime
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers, response
from .models import Language, Category, Categorydescription, Photo, PhotoDescription, Genocide, GenocideDescription
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .settings import MEDIA_ROOT


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User

    @classmethod
    def get_days_since_joined(cls, obj):
        return (now() - obj.date_joined).days


class LanguageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10)
    default = serializers.BooleanField(default=False)

    class Meta:
        fields = ('name', 'default')
        model = Language

    @classmethod
    def create_lang(cls, data):
        name = data['name']
        default = data['default']
        check = Language.objects.filter(name=name)
        if check:
            check = check[0]
            if check.default != default:
                check.default = default
                check.save()
            content = {"id": check.id, "name": check.name, "default": check.default}
            return content
        new_lang = Language.objects.create(name=name, default=default)
        new_lang.save()
        content = {"id": new_lang.id, "name": new_lang.name, "default": new_lang.default}
        return content


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        # token['access_token'] = str(token.access_token)
        return token


class PhotoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    image = serializers.ImageField()
    description = serializers.CharField()
    language_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    class Meta:
        fields = ('name', 'image', 'description', 'language_id', 'category_id')
        model = Photo

    @classmethod
    def create_photo(cls, data, ):
        name = data['name']
        language_id = data['language_id']
        category_id = data['category_id']
        description = data['description']
        image = data['image']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            content = {"meta": {"status": "error", "error": "No such category found."}}
            return content
        try:
            lang = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            content = {"meta": {"status": "error", "error": "No such language found."}}
            return content
        image_name = uuid.uuid4()
        photo_path = f'{MEDIA_ROOT}{category.id}/{image_name}.png'
        with open(photo_path, "wb") as f:
            f.write(image.read())
        # TODO change http://127.0.0.1:8000
        photo_url = f'http://127.0.0.1:8000/media/{category.id}//{image_name}.png'
        photo = Photo.objects.create(image=photo_url, category_id=category, created=datetime.now())
        photo.save()
        file_stats = os.stat(photo_path)
        size = file_stats.st_size
        photo_description = PhotoDescription.objects.create(name=name, description=description,
                                                            language_id=lang, photo_id=photo,
                                                            size=size)
        photo_description.save()
        content = {"name": photo_description.name, "language_id": photo_description.language_id.id,
                   "description": photo_description.description,
                   "category_id": photo_description.photo_id.category_id.id}
        return content
