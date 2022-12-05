import logging
import os
import shutil
from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Language, Photo, Category, Categorydescription, PhotoDescription, Genocide, GenocideDescription
from .pagination import CustomPagination
from .serializers import LanguageSerializer, PhotoSerializer
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


class CategoryByNameView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request, category):
        print(category)
        try:
            cat = Category.objects.get(name=category)
        except Category.DoesNotExist:
            content = {"meta": {"status": "error", "error": "No such category found."}}
            return content
        inner_dict = list()
        cat_desc = Categorydescription.objects.filter(category_id=cat.id)
        for el in cat_desc:
            d = {"language_id": el.language_id.id, "name": el.name, "description": el.description}
            inner_dict.append(d)
        result = {'id': cat.id, 'internalizations': inner_dict}
        return JsonResponse(result)


class CategoryAddView(APIView):

    permission_classes = [IsAuthenticated, ]

    @classmethod
    def post(cls, request):
        print(request.data)
        internalization = request.data['internalization']
        name = internalization['name']
        language_id = internalization['language_id']
        description = internalization['description']
        try:
            category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            category = Category.objects.create(name=name)
        try:
            lang = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            content = {"meta": {"status": "error", "error": "No such language found."}}
            return content
        new_cat_description = Categorydescription.objects.create(name=name, description=description,
                                                                 language_id=lang, category_id=category)
        category.save()
        new_cat_description.save()

        cats = Categorydescription.objects.filter(category_id=category)
        result = list()
        for c in cats:
            d = {"name": c.name, "language_id": c.language_id.id, "description": c.description}
            result.append(d)
        content = {"id": category.id, "internalizations": result}
        return Response(content)


class GenocideAddView(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request):
        print(request.data)
        internalization = request.data['internalization']
        genocide = Genocide.objects.create()
        for i in internalization:
            language_id = i['language_id']
            text = i['text']
            try:
                lang = Language.objects.get(id=language_id)
            except Language.DoesNotExist:
                continue
            new_gen_description = GenocideDescription.objects.create(text=text, language_id=lang,
                                                                     genocide_id=genocide)
            genocide.save()
            new_gen_description.save()
        gens = GenocideDescription.objects.filter(genocide_id=genocide)
        result = list()
        for g in gens:
            d = {"language_id": g.language_id.id, "text": g.text}
            result.append(d)
        created = datetime.strftime(genocide.created, "%d.%m.%Y %H:%M.%z")
        content = {"id": genocide.id, "latest": genocide.latest, "createdAt": created, "internalizations": result}
        return Response(content)


class PhotoView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        paginator = CustomPagination()
        direction = request.GET.get('direction')
        category = request.GET.get("category")
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


class GenocideView(APIView):

    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        queryset = Genocide.objects.all()
        genocide = list()
        if queryset is None:
            context = None
            return Response(context)
        for el in queryset:
            description = GenocideDescription.objects.filter(genocide_id=el.id)
            inner_dict = list()
            for d in description:
                created = datetime.strftime(d.created, "%d.%m.%Y %H:%M.%z")
                dic = {"language_id": d.language_id.id, "text": d.text, "created": created}
                inner_dict.append(dic)
            d = {'id': el.id, 'internalizations': inner_dict, 'latest': el.latest}
            genocide.append(d)
        return Response(genocide)







