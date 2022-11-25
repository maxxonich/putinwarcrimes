import logging
import os
import shutil
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Language, Photo, Category, Categorydescription, PhotoDescription
from .pagination import CustomPagination
from .serializers import LanguageSerializer, PhotoSerializer, CategorySerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .settings import MEDIA_ROOT


@receiver(post_save, sender=Category)
def create_folder(sender, instance, created, **kwargs):
    """ Create folder for photo files """
    if created:
        path = f'{MEDIA_ROOT}{instance.id}/'
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)


@receiver(pre_delete, sender=Category, )
def delete_folder(sender, instance, *args, **kwargs):
    """ Deletes folder and photo files """
    path = f'{MEDIA_ROOT}{instance.id}/'
    shutil.rmtree(path)


@receiver(pre_delete, sender=Photo, )
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes file from filesystem. """
    path = instance.image
    if os.path.isfile(path):
        os.remove(path)
    else:
        logging.info("File has been already deleted ")


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


class PhotoAddView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PhotoSerializer

    @classmethod
    def post(cls, request):
        context = cls.serializer_class.create_photo(request.data)
        return Response(context)


class CategoryView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        queryset = Category.objects.all()
        categories = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            description = Categorydescription.objects.filter(category_id=el.id)
            inner_dict = list()
            for d in description:
                dic = {"language_id": d.language_id.id, "name": d.name, "description": d.description}
                inner_dict.append(dic)
            d = {'id': el.id, 'internalizations': inner_dict, }
            categories.append(d)
        return Response(categories)


class CategoryAddView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]

    @classmethod
    def post(cls, request):
        content = cls.serializer_class.create_category(request.data)
        return Response(content)


class PhotoView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        paginator = CustomPagination()
        direction = request.GET.get('direction')
        category = request.GET.get("categories")
        if category:
            queryset = Photo.objects.filter(category_id=category)
        else:
            queryset = Photo.objects.all()
        if direction == 'dsc':
            queryset = queryset.order_by('-created')
        elif direction == 'asc':
            queryset = queryset.order_by('created')
        photos = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            description = PhotoDescription.objects.filter(photo_id=el.id)
            inner_dict = list()
            for d in description:
                dic = {"language_id": d.language_id.id, "name": d.name, "text": d.description,
                       "size": d.size}
                inner_dict.append(dic)
                d = {'language_id': el.id, 'internalizations': inner_dict, 'path': el.image,
                     'category_id': el.category_id.id}
                photos.append(d)
        result_page = paginator.paginate_queryset(photos, request)
        print(result_page)
        return Response(result_page)
