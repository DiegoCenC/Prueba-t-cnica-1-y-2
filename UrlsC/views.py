import random
import string
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Urls
from .serializers import UrlsSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ViewSet para manejar las URLs acortadas
@method_decorator(csrf_exempt, name='dispatch')
class UrlsViewSet(viewsets.ModelViewSet):
    queryset = Urls.objects.all()
    serializer_class = UrlsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("Usuario autenticado:", self.request.user)  # Imprime el usuario autenticado
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError({'error': 'Usuario no autenticado'})

        max_attempts = 5  # Limitar el número de intentos
        attempt = 0

        while attempt < max_attempts:
            shortened_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            shortened_url = f"http://127.0.0.1:8000/{shortened_code}"

            try:
                with transaction.atomic():
                    serializer.save(shortened_url=shortened_url, created_by=self.request.user)
                    return
            except IntegrityError:
                attempt += 1

        raise serializers.ValidationError({'error': 'No se pudo generar una URL acortada única.'})

# Vista para registrar usuarios
class RegisterUser(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            },
            required=['username', 'password'],
            example={
                'username': 'ejemplo_usuario',
                'password': '123456',
            }
        ),
        responses={201: 'Usuario registrado correctamente', 400: 'Error en la solicitud'}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'El username ya está en uso'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)

        return Response({'message': 'Usuario registrado correctamente', 'token': token.key}, status=status.HTTP_201_CREATED)

# Vista para iniciar sesión
class LoginUser(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            },
            required=['username', 'password'],
            example={
                'username': 'ejemplo_usuario',
                'password': '123456',
            }
        ),
        responses={200: 'Inicio de sesión exitoso', 400: 'Error en la solicitud', 401: 'Credenciales inválidas'}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username y password son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Inicio de sesión exitoso', 'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

# Vista para redireccionar a la URL original
def redirect_to_original(request, code):
    # Buscar la URL acortada en la base de datos
    shortened_url = f"http://127.0.0.1:8000/{code}"
    url_record = get_object_or_404(Urls, shortened_url=shortened_url)

    # Incrementar el contador de vistas
    url_record.view_count += 1
    url_record.save()

    # Redirigir a la URL original
    return HttpResponseRedirect(url_record.original_url)

# Función para renderizar el formulario HTML
def shorten_url_form(request):
    return render(request, 'shorten_url.html')
