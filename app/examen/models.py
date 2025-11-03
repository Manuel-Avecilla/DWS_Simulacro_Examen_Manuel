from django.db import models

# Create your models here.
#------------------------------- Coche ------------------------------------------ 
class Coche(models.Model): 
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    anyo_lanzamiento = models.PositiveIntegerField()


#------------------------------- Itv ------------------------------------------ 
class Itv(models.Model):
    ESTADOS = [ 
        ('A', 'Aceptada'), 
        ('P', 'Pendiente'), 
        ('R', 'Rechazada'), 
    ]  
    resultado = models.CharField(max_length=1, choices=ESTADOS)
    numero_itv = models.PositiveIntegerField()
    
    coches = models.ManyToManyField(Coche, through="Revision", related_name='itvCoche')

#------------------------------- Mecanico ------------------------------------------ 
class Mecanico(models.Model): 
    
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    antiguedad = models.PositiveIntegerField()


#------------------------------- Taller ------------------------------------------ 
class Taller(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()


#------------------------------- Revision ------------------------------------------ 
class Revision(models.Model): 
    
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, related_name='revisionCoche')
    itv = models.ForeignKey(Itv, on_delete=models.CASCADE, related_name='revisionItv')
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE, related_name='revisionMecanico')
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='revisionTaller')
    
    kilometraje = models.PositiveIntegerField()
    fecha_revision = models.DateField(null=True, blank=True)
    
    ESTADOS = [ 
        ('AP', 'Apta'), 
        ('CF', 'Con fallos'), 
        ('GR', 'Grave'), 
    ] 
    resultado = models.CharField(max_length=2, choices=ESTADOS)