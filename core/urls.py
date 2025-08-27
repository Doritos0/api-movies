from django.urls import path
from .views import lista_peliculas, detalle_pelicula, lista_usuarios, detalle_usuario, lista_usuario_peliculas, detalle_usuario_pelicula

urlpatterns=[
     path('lista_peliculas/',lista_peliculas, name="lista_peliculas"),
    path('detalle_pelicula/<id>', detalle_pelicula, name="detalle_pelicula"),
     path('lista_usuarios/',lista_usuarios, name="lista_usuarios"),
    path('detalle_usuario/<id>', detalle_usuario, name="detalle_usuario"),
     path('lista_usuario_peliculas/',lista_usuario_peliculas, name="lista_usuario_peliculas"),
    path('detalle_usuario_pelicula/<id>', detalle_usuario_pelicula, name="detalle_usuario"),
]