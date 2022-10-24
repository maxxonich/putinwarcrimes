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

# class CategorySerializer(serializers.ModelSerializer):
#
#      class Meta :
#          fields= ('name', 'description')
#          model = Category
#
#      @classmethod
#      def get_category(cls):



