from rest_framework import serializers
from .models import Pelicula, Usuario, UsuarioPelicula


class PeliculaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__' 


class UsuarioSerializer (serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__' 


class UsuarioPeliculaSerializer (serializers.ModelSerializer):
    class Meta:
        model = UsuarioPelicula
        fields = '__all__' 



'''
class ProductoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
'''
