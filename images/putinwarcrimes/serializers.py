from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers, response
from .models import Language, Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response


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


class CategorySerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    category_id = serializers.IntegerField()


    class Meta:
        fields = ('language_id', 'name', 'description', 'language_id', 'category_id')
        model = Category

    @classmethod
    def get_category(cls):
        queryset = CategorySerializer.objects.all()




    @classmethod
    def create_category(cls, data):
        name = data['name']
        language_id = data['language_id']
        description = data['description']
        check = Category.objects.filter(name=name, description=description, language_id=language_id)
        if check is None:
            return None
        new_category = Category.objects.create(name=name, )
        new_category.save()
        content = {"name": new_category.name, "language_id": new_category.language_id,
                   "description": new_category.description}
        return content



# class PhotoSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     image = serializers.ImageField(upload_to='files/front/upload/', height_field=None, width_field=None, max_length=100)
#     description = serializers.CharField()
#     language_id = serializers.IntegerField()
#
#     @classmethod
#     def create_photo(cls, data):
#         name = data['internalization']['name']

