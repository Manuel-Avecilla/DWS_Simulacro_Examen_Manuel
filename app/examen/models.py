from django.db import models
from django.contrib.auth.models import AbstractUser

#------------------------------- USUARIO ------------------------------------------
class Usuario(AbstractUser):
    
    ADMINISTRADOR = 1
    TECNICO = 2
    USUARIO = 3
    
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (TECNICO, 'Tecnico'),
        (USUARIO, 'Usuario'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=1,
    )
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

#------------------------------- TECNICO ------------------------------------------
class Tecnico(models.Model):
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='tecnico')
    
    edad = models.PositiveIntegerField(blank=True, null=True)
    puesto = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return f"Tecnico: {self.usuario.username}"



