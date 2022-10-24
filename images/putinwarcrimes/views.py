from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Language, Photo
from .serializers import LanguageSerializer
# from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class LanguageView(APIView):

    @classmethod
    def get(cls, request):
        queryset = Language.objects.all()
        langs = list()
        print(queryset)
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            d = {'id': el.id, 'name': el.name, 'default': el.default}
            langs.append(d)
        print(langs)  # [{'id': 1, 'name': 'ukr', 'default': False}, {'id': 2, 'name': 'eng', 'default': True}]
        context = langs
        return Response(context)


class LanguageAddView(APIView):
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated, ]

    @classmethod
    def post(cls, request):
        print(request.data)
        content = cls.serializer_class.create_lang(request.data)
        return JsonResponse(content)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class PhotoView(APIView):

    @classmethod
    def get (cls,request):
        queryset = Photo.objects.all()
        photos = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            d = {'id': el.id, 'name': el.name, 'description': el.description,'language': el.language}
            photos.append(d)



