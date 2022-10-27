from django.contrib.gis.gdal import field
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Language, Photo, Category, Categorydescription, PhotoDescription
from .serializers import LanguageSerializer
#  from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
import os


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
            d = {"id": el.id, "name": el.name, "default": el.default}
            langs.append(d)
        print(
            langs
        )  # [{'id': 1, 'name': 'ukr', 'default': False}, {'id': 2, 'name': 'eng', 'default': True}]
        context = langs
        return Response(context)


class LanguageAddView(APIView):
    serializer_class = LanguageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @classmethod
    def post(cls, request):
        print(request.data)
        content = cls.serializer_class.create_lang(request.data)
        return JsonResponse(content)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class PhotoAddView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @classmethod
    def post(cls, request):
        path_to_file = "files/front/upload/"
        file_stats = os.stat(path_to_file)
        size = int(file_stats.st_size)
        print(size)
        new_photo = Photo.objects.create(size=size)
        return Response("photos")


class CategoryView(APIView):
    @classmethod
    def get(cls, request):
        queryset = Category.objects.all()
        categories = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            print(el)
            description = Categorydescription.objects.filter(category_id=el.id,)
            inner_dict = list()
            sub_dict = {}
            for d in description:
                # if field.is_relation:
                #     sub_dict[field.name] = get(
                #         getattr(object, field.name))
                dic = {"language_id": d.language_id, "name": d.name, "description": d.description,}
                inner_dict.append(dic)
            d = {'id': el.id, 'internalization': inner_dict, }
            categories.append(d)
        return Response(categories)

#add a lang.id to photo and category


class PhotoView(APIView):
    @classmethod
    def get(cls, request):
        queryset = Photo.objects.all()
        photos = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            description = PhotoDescription.objects.filter(photo_id=el.id)
            inner_dict = list()
            for d in description:
                dic = {"language_id": d.language_id, "name": d.name, "description": d.description, "size": d.size, "created": d.created,}
                inner_dict.append(dic)
            d = {'language_id': el.id, 'internalization': inner_dict}
            photos.append(d)
        return Response(photos)
