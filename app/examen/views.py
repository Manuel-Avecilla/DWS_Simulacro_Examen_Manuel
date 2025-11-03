from django.shortcuts import render
from django.views.defaults import page_not_found
from django.db.models import Q 

from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')
#-----------------------------------------------------------------
def dame_animal(request, id_animal):
    
    animal = (
        Animal.objects
        .select_related("tipo")
        .get(id=id_animal)
    )
    
    """
    animal = (Animal.objects.raw(
    "SELECT * FROM examen_animal ani "
    + " JOIN examen_tipo ti ON ti.id = ani.tipo_id "
    + " WHERE ani.id = %s",[id_animal])[0]
    )
    """
    
    return render(request, 'animal.html',{'Animal_Mostrar':animal})

#-----------------------------------------------------------------
def dame_revision(request, id_animal):
    
    revision = (
        Revision.objects
        .select_related("animal")
        .filter(animal_id = id_animal)
        .order_by("-fecha_revision")[:1].get()
    )
    
    """
    revision = (Revision.objects.raw(
    "SELECT * FROM examen_revision re "
    + " JOIN examen_animal ani ON ani.id = re.animal_id "
    + " WHERE ani.id = %s"
    + " ORDER BY re.fecha_revision DESC "
    + " LIMIT 1 " 
    ,[id_animal])[0]
    )
    """
    
    return render(request, 'revision.html',{'Revision_Mostrar':revision})
#-----------------------------------------------------------------

def dame_alimales_revisiones(request):
    
    animales = (
        Animal.objects
        .select_related("tipo")
        .filter(Q(revisionAnimal__resultado = "CI")|Q(revisionAnimal__resultado = "RR"))
        .all()
    )
    
    return render(request, 'lista_animales.html',{'Animales_Mostrar':animales})
#-----------------------------------------------------------------

def dame_tipo_sin_animales(request):
    
    tipos = (
        Tipo.objects
        .filter(tipoAnimal = None)
        .all()
    )
    """
    
    tipos = (Tipo.objects.raw(
    "SELECT * FROM examen_tipo ti "
    + " LEFT JOIN examen_animal ani ON ani.tipo_id = ti.id "
    + " WHERE ani.tipo_id IS NULL "
    ))
    
    """

    return render(request, 'lista_tipos.html',{'Tipos_Mostrar':tipos})
#-----------------------------------------------------------------


def dame_alerta_pendiente_2025(request):
    """
    alertas = (
        Alerta.objects
        .select_related("revision__animal")
        .filter(estado = "P" , fecha_creacion__year = 2025)
        .all()
    )
    
    """
    
    alertas = (Alerta.objects.raw(
    "SELECT * FROM examen_alerta aler "
    + " JOIN examen_revision re ON re.id = aler.revision_id "
    + " JOIN examen_animal ani ON ani.id = re.animal_id "
    + " WHERE aler.estado = 'P' "
    + " AND strftime('%%Y', aler.fecha_creacion) = '2025' "
    ))
    
    
    
    return render(request, 'lista_alerta.html',{'Alertas_Mostrar':alertas})



# Errores
def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)