from django.db import models

# Create your models here.

#------------------------------- Tipo ------------------------------------------
class Tipo(models.Model):
    
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    nivel_prioridad = models.PositiveIntegerField()
    
    def __str__(self):
        return self.nombre


#------------------------------- Animal ------------------------------------------
class Animal(models.Model):
    
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    # Relacion (1:N)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='tipoAnimal')

    def __str__(self):
        return self.nombre


#------------------------------- Revision ------------------------------------------
class Revision(models.Model):
    
    fecha_revision = models.DateField(null=True, blank=True)
    nombre_tecnico = models.CharField(max_length=150, unique=True)
    
    ESTADOS = [
        ('CO', 'Correcto'),
        ('CI', 'Con incidencias'),
        ('RR', 'Requiere reparación'),
    ]
    resultado = models.CharField(max_length=2, choices=ESTADOS)
    
    # Relacion (1:N)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='revisionAnimal')

    def __str__(self):
        return self.nombre_tecnico


#------------------------------- Alerta ------------------------------------------
class Alerta(models.Model):
    
    fecha_creacion = models.DateField(null=True, blank=True)
    mensaje = models.TextField(blank=True)
    
    ESTADOS = [
        ('P', 'Pendiente'),
        ('R', 'Resuelta'),
    ]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    
    # Relacion (1:N)
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE, related_name='alertaRevision')
    
    def __str__(self):
        return self.mensaje