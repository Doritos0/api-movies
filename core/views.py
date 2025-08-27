from django.shortcuts import render
from .models import Pelicula, Usuario, UsuarioPelicula
from .serializers import PeliculaSerializer, UsuarioPeliculaSerializer, UsuarioSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

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
            serializer = PeliculaSerializer(data=request.data)

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
        serializer = UsuarioSerializer(data = request.data)
        print("❤️ ", serializer)

        if serializer.is_valid():
            serializer = UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Comprobar si ya existe película con mismo año y director
            usuario_existe = Usuario.objects.filter(user=user).exists()

            if usuario_existe:
                return Response(
                    {"error": "Este nombre de usuario ya esta en uso"},
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