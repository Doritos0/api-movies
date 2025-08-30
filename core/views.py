from django.shortcuts import render
from .models import Pelicula, Usuario, UsuarioPelicula
from .serializers import PeliculaSerializer, UsuarioPeliculaSerializer, UsuarioSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings

# Create your views here.

#TABLA PELICULA GET, POST, PATCH, DELETE

@api_view(['GET', 'POST'])
def lista_peliculas (request):
    if request.method == 'GET':
        query = Pelicula.objects.all()
        serializer = PeliculaSerializer(query, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PeliculaSerializer(data = request.data)
        print("❤️ ", serializer)

        if serializer.is_valid():
            anio = serializer.validated_data['anio']
            director = serializer.validated_data['director']

            # Comprobar si ya existe película con mismo año y director
            pelicula_existe = Pelicula.objects.filter(anio=anio, director=director).exists()

            if pelicula_existe:
                return Response(
                    {"error": "Ya existe una película con este año y director"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PATCH','DELETE'])
def detalle_pelicula (request,id):
    try:
        pelicula = Pelicula.objects.get(id_pelicula=id)

    except Pelicula.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PeliculaSerializer(pelicula)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = PeliculaSerializer(pelicula, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        pelicula.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


#TABLA USUARIO GET, POST, PATCH, DELETE
@api_view(['GET', 'POST'])
def lista_usuarios (request):
    if request.method == 'GET':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':

        #HAGO UNA COPIA DEL REQUEST PARA TRABAJAR CON ESTOS DATOS SIN MANIPULAR LOS ORIGINALES
        data= request.data.copy()
        user = data.get('user')
        password = data.get('password')

        #LOS PRINTEO PARA VER QUE INFORMACION TIENEN
        print(user)
        print(password)

        #IF PARA CORROBORAR QUE ES UN USUARIO NUEVO
        if Usuario.objects.filter(user = user).exists():
            return Response(
                {"Error": "Este usuario ya existe"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 4 or len(password) > 30:
            '''

            RETURN RESPONSE MAL EJECUTADO (SINTAXIS ERRONEA)

            return Response()(
                {"Error":"Contraseña debe tener entre 4 y 30 caracteres"},
                status=status.HTTP_400_BAD_REQUEST
            )
            '''
            return Response(
                {"Error": "Contraseña debe tener entre 4 y 30 caracteres"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        #CAMBIO EL PASSWORD ORIGINAL DE DATA YA HASHEADO

        data['password'] = make_password(password)

        #LO SERIALIZO
        serializer = UsuarioSerializer(data = data)

        #IF PARA GUARDAR EL NUEVO USUARIO
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET','PATCH','DELETE'])
def detalle_usuario (request, id):
    try:
        usuario = Usuario.objects.get(id_usuario=id)

    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

#TABLA INTERMEDIA
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lista_usuario_peliculas(request):
    if request.method == 'GET':
        query = UsuarioPelicula.objects.all()
        serializer = UsuarioPeliculaSerializer(query, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuarioPeliculaSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            pelicula = serializer.validated_data['pelicula']

            # Evitar duplicados
            relacion, created = UsuarioPelicula.objects.get_or_create(
                usuario=usuario,
                pelicula=pelicula,
                defaults={
                    'estado_pelicula': serializer.validated_data.get('estado_pelicula', 0),
                    'puntuacion': serializer.validated_data.get('puntuacion', 0)
                }
            )

            if not created:
                return Response(
                    {"error": "Esta relación usuario-película ya existe"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = UsuarioPeliculaSerializer(relacion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def detalle_usuario_pelicula(request, id):
    try:
        relacion = UsuarioPelicula.objects.get(id=id)
    except UsuarioPelicula.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retorna los datos de la relación
        serializer = UsuarioPeliculaSerializer(relacion)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # Actualiza parcialmente la relación (estado, puntuación, etc.)
        serializer = UsuarioPeliculaSerializer(relacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Elimina la relación usuario-película
        relacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#ENDPOINT PARA LOGIN
@api_view(['POST'])
def login_usuario(request):
    data = request.data.copy()
    user = data.get('user')
    password = data.get('password')

    print("este user llega ", user)
    print("este pass llega ", password)

    if not user or not password:
        return Response(
            {"error": "Usuario y contraseña son requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        usuario = Usuario.objects.get(user=user)
    except Usuario.DoesNotExist:
        return Response(
            {"error": "Usuario no existe"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Comparar contraseña con la almacenada (hash)
    if check_password(password, usuario.password):
        
        refresh = RefreshToken.for_user(usuario)
        access = refresh.access_token

        print("REFRESCO ",refresh)
        print("ACCESS ",access)


        response = JsonResponse({
            "mensaje": f"Bienvenido {usuario.user}",
            "token" : str(refresh)
        })

        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            samesite='Strict', 
            secure=False,
            max_age=7*24*60*60         
        )

        # Opcional: también puedes mandar access token en cookie
        response.set_cookie(
            key='access',
            value=str(access),
            httponly=True,
            samesite='Strict',
            secure=False,
            max_age=3600
        )

        return response

        #return Response({
            #"refresh": str(refresh),
            #"access": str(access),
            #"data": serializer.data}, status=status.HTTP_200_OK)


        #return Response({"bienvenido"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Contraseña incorrecta"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    """
    Devuelve el usuario logueado según el token enviado en cookies.
    """
    user = request.user  # JWTAuthentication ya asigna request.user
    serializer = UsuarioSerializer(user)
    return Response({"data": serializer.data})


#ENDPOINTS PARA REFRESCO DE TOKENS
@api_view(['POST'])
def refresh_access(request):
    """
    Lee el refresh token desde la cookie 'refresh', genera un nuevo access token
    y lo devuelve en cookie 'access'. Retorna 401 si el refresh es inválido.
    """
    refresh_token = request.COOKIES.get('refresh')
    if not refresh_token:
        return Response({"error": "Refresh token no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_token)
        new_access = refresh.access_token

        response = JsonResponse({"detail": "Access renovado"})
        # Ponemos el nuevo access en cookie (ajusta secure/samesite según ambiente)
        response.set_cookie(
            key='access',
            value=str(new_access),
            httponly=True,
            samesite='Strict',   # en dev puedes usar 'Lax' si da problemas
            secure=False,
            max_age=3600  # 1 hora por ejemplo
        )
        return response

    except TokenError:
        return Response({"error": "Refresh token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)