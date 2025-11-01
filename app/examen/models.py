from django.db import models

# Create your models here.

#------------------------------- USUARIO ------------------------------------------
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100) 
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario

#------------------------------- CUENTA_BANCARIA ------------------------------------------
class CuentaBancaria(models.Model):
    
    # Relacion 1:1 con Usuario (Tiene)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuentaBancaria')
    
    BANCOS = [
        ('CX', 'Caixa'),
        ('BB', 'BBVA'),
        ('UN', 'UNICAJA'),
        ('IN', 'ING'),
    ]
    banco = models.CharField(max_length=2, choices=BANCOS)
    numero = models.PositiveIntegerField()
    
    def __str__(self):
        return self.usuario.nombre_usuario

#------------------------------- MOVIL ------------------------------------------
class Movil(models.Model):
    
    # Relacion N:N con Usuario (Votar)
    votos = models.ManyToManyField(Usuario, through='Votar', related_name='votos_recibidos')
    
    modelo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.modelo


#------------------------------- VOTAR (Relacion) ------------------------------------------
class Votar(models.Model):
    # FK de la relacion N:N con Usuario - Movil
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='votar_usuario')
    movil = models.ForeignKey(Movil, on_delete=models.CASCADE, related_name='votar_movil')
    
    puntuacion = models.PositiveIntegerField()
    comentario = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comentario