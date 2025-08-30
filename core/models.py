from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ------------------------
# Manager personalizado
# ------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, user, password=None, **extra_fields):
        if not user:
            raise ValueError("El campo 'user' es obligatorio")

        usuario = self.model(user=user, **extra_fields)
        usuario.set_password(password)   # <- encripta la contraseña
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, user, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(user, password, **extra_fields)


# ------------------------
# Modelo Película
# ------------------------
class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    anio = models.IntegerField()
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


# ------------------------
# Modelo Usuario (Custom)
# ------------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    # campos de tu diseño original
    tipo = [
        (1, 'Admin'),
        (0, 'Usuario'),
    ]
    id = models.AutoField(primary_key=True)
    id_tipo = models.IntegerField(choices=tipo, default=0)

    user = models.CharField(max_length=25, unique=True)  # será el campo para login
    email = models.EmailField(unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)

    # campos requeridos por Django
    is_active = models.BooleanField(default=True)   # si el usuario está activo
    is_staff = models.BooleanField(default=False)   # acceso al admin

    # relación M2M con películas
    peliculas_vistas = models.ManyToManyField(
        Pelicula,
        through='UsuarioPelicula',
        related_name='vista_por'
    )

    # manager
    objects = UsuarioManager()

    # configuración de login
    USERNAME_FIELD = "user"   # usamos 'user' para iniciar sesión
    REQUIRED_FIELDS = ["email"]  # se pedirá además el email al crear superusuarios

    def __str__(self):
        return self.user


# ------------------------
# Relación Usuario-Película
# ------------------------
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
        default=0
    )
    
    class Meta:
        unique_together = ('usuario', 'pelicula')

    def __str__(self):
        return f"{self.usuario.user} - {self.pelicula.titulo} ({self.estado_pelicula}, {self.puntuacion})"
