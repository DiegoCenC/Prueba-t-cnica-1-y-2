from django.urls import path, re_path
from .views import UrlsViewSet, shorten_url_form, RegisterUser, LoginUser, redirect_to_original
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'urls', UrlsViewSet)

urlpatterns = [
    path('shorten/', shorten_url_form, name='shorten-url-form'),
    path('register/', RegisterUser.as_view(), name='register-user'),
    path('login/', LoginUser.as_view(), name='login-user'),
    re_path(r'^(?P<code>[a-zA-Z0-9]{6})/$', redirect_to_original, name='redirect-to-original'),  # Ruta de redirección para códigos de 6 caracteres
]

urlpatterns += router.urls
