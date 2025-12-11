from django.db import models
from django.contrib.auth.models import AbstractUser

# Deben existir dos grupos de usuarios: "Organizadores" y "Asistentes".

#------------------------------- USUARIO ------------------------------------------
class Usuario(AbstractUser):
    
    ADMINISTRADOR = 1
    ORGANIZADOR = 2
    ASISTENTE = 3
    
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (ORGANIZADOR, 'Organizador'),
        (ASISTENTE, 'Asistente'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=1,
    )
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


#------------------------------- ORGANIZADOR ------------------------------------------
class Organizador(models.Model):
    
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='Organizador')
    
    codigo_empleado = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return f"Organizador: {self.usuario.username}"


#------------------------------- ASISTENTE ------------------------------------------
class Asistente(models.Model):
    
    # Relacion 1:1 con Usuario
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='Asistente')
    
    edad = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Asistente: {self.usuario.username}"


#------------------------------- CATEGORIA ------------------------------------------
class Categoria(models.Model): 
    nombre = models.CharField(max_length=50, unique=True) 
    descripcion = models.TextField(blank=True) 
    
    def __str__(self): 
        return self.nombre 


#------------------------------- SALA ------------------------------------------
class Sala(models.Model): 
    nombre = models.CharField(max_length=100) 
    capacidad_maxima = models.IntegerField() 
    tiene_proyector = models.BooleanField(default=False) 
    
    def __str__(self): 
        return self.nombre


#------------------------------- EVENTO ------------------------------------------
class Evento(models.Model):
    
    # Relacion N:1 con Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='eventoCategoria')
    # Relacion N:1 con Sala
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='eventoSala')
    # Relacion N:1 con Creador
    creador = models.ForeignKey(Organizador, on_delete=models.CASCADE, related_name='creador')
    
    titulo = models.CharField(max_length=150,unique=True)
    descripcion = models.TextField()
    
    aforo = models.IntegerField() 
    
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    
    
    def __str__(self): 
        return self.titulo