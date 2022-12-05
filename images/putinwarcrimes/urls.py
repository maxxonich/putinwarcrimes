"""images URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from .admin import GenocideDescription
from .views import LanguageView, LanguageAddView, MyObtainTokenPairView, PhotoAddView, CategoryView, PhotoView, \
    CategoryAddView, CategoryByNameView, GenocideView, GenocideAddView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/langs/', LanguageView.as_view(), name='lang'),
    path('api/add_lang/', LanguageAddView.as_view(), name='lang_add'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # re_path(r"data/(?P<pk>\d+')('?P<response_type>\w+'), cdxcomposites_detail)", PhotoView.as_view(),
    #         name='photo_show'),
    path('api/photos/', PhotoView.as_view(), name='photos'),
    path('api/add_photos/', PhotoAddView.as_view(), name='add_photo'),
    path('api/categories/', CategoryView.as_view(), name='category'),
    path('api/categories/by_name/<category>', CategoryByNameView.as_view(), name='by_name_category'),
    path('api/add_categories/', CategoryAddView.as_view(), name='category'),
    path('api/api/descriptions/latest', GenocideView.as_view(), name="genocide"),
    path('api/descriptions/', GenocideAddView.as_view(), name="add_genocide"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
