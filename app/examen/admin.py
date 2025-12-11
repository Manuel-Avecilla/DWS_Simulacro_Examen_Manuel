from django.contrib import admin

# Register your models here.
from .models import Evento, Categoria, Sala, Usuario, Organizador, Asistente

admin.site.register(Evento)
admin.site.register(Categoria) 
admin.site.register(Sala) 
admin.site.register(Usuario) 
admin.site.register(Organizador)
admin.site.register(Asistente)