from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

# Create your models here.

class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    anio = models.IntegerField()
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
    
class Usuario(models.Model):
    tipo = [
        (1, 'Admin'),
        (0, 'Usuario'),
    ]
    id_tipo = models.IntegerField(choices=tipo)
    id_usuario = models.AutoField(primary_key=True)
    user = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=150, validators=[MinLengthValidator(4)] )
    peliculas_vistas = models.ManyToManyField(
        Pelicula,
        through = 'UsuarioPelicula',
        related_name = 'vista_por'
    )
 
    def __str__(self):
        return self.user


class UsuarioPelicula(models.Model):
    id = models.AutoField(primary_key=True)
    estado = [
        (0, 'No Vista'),
        (1, 'Vista'),
    ]
    estado_pelicula = models.IntegerField(choices=estado)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0)
    
    class Meta:
        unique_together = ('usuario', 'pelicula')

    def __str__(self):
        return f"{self.usuario.user} - {self.pelicula.titulo} ({self.estado}, {self.puntuacion})"

'''

from django.db import models
from django.core.exceptions import ValidationError
import json

# Create your models here.
class TipoProducto(models.Model):
    TipoProducto = [
        ('Herramientas Manuales','Herramientas Manuales'),#1- Herramientas Manuales
        ('Materiales Basicos', 'Materiales Basicos'),#2- Materiales Basicos
        ('Equipo de Seguridad', 'Equipo de Seguridad'), #3- Equipo de Seguridad
        ('Tornillos y Anclajes', 'Tornillos y Anclajes'), #4-Tornillos y Anclajes
        ('Fijaciones y Adhesivos', 'Fijaciones y Adhesivos'), #5-Fijaciones y Adhesivos
        ('Equipos de Medicion', 'Equipos de Medicion'), #6-Equipos de Medicion
    ]
    id_tipo = models.CharField(choices=TipoProducto, primary_key=True, max_length=50)

    def __str__(self):
        return self.id_tipo

 #   def __str__(self):
    #    return str(self.tipo_nombre)


class Producto(models.Model):
    Oferta = [
        (1, 'Si'),
        (0, 'No'),
    ]
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    oferta = models.IntegerField(choices=Oferta)
    porcentaje = models.IntegerField(null=True, blank=True)
    id_tipo = models.ForeignKey('TipoProducto', on_delete=models.CASCADE)'''