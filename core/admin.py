from django.contrib import admin
from .models import Pelicula, Usuario, UsuarioPelicula

# Register your models here.

admin.site.register(Pelicula)
admin.site.register(Usuario)
admin.site.register(UsuarioPelicula)