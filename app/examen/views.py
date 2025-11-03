from django.shortcuts import render
from django.views.defaults import page_not_found
from django.db.models import Q , Prefetch, Avg, Max, Min, Count
from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html')


def dame_ultima_revision(request, id_coche):
    
    revision = (
        Revision.objects
        .select_related("coche","itv","mecanico","taller")
        .filter(coche_id = id_coche) 
        .order_by("-fecha_revision")[:1].get() 
    )
    
    """ 
    revision = (Revision.objects.raw( 
    "SELECT * FROM examen_revision re " 
    + " JOIN examen_coche co ON co.id = re.coche_id "
    + " JOIN examen_itv itv ON itv.id = re.itv_id "
    + " JOIN examen_mecanico me ON me.id = re.mecanico_id "
    + " JOIN examen_taller ta ON ta.id = re.taller_id "
    + " WHERE re.coche_id = %s " 
    + " ORDER BY re.fecha_revision DESC " 
    + " LIMIT 1 " 
    ,[id_coche] 
    )[0]) 
    """
    
    return render(request,'revision.html',{'Revision_Mostrar':revision})

#---------------------------------------------------------------------------

def dame_coche_revision_grave(request):
    
    coches = (
        Coche.objects
        .filter(revisionCoche__resultado = "GR")
        .all()
    )
    
    """ 
    coches = (Coche.objects.raw( 
    "SELECT * FROM examen_coche co "
    + " JOIN examen_revision re ON co.id = re.coche_id "
    + " WHERE re.resultado = 'GR' " 
    )) 
    """
    
    return render(request,'lista_coche.html',{'Coches_Mostrar':coches})

#---------------------------------------------------------------------------
def dame_talleres_sin_revision(request):
    
    talleres = (
        Taller.objects
        .filter(revisionTaller = None)
        .all()
    )
    
    """ 
    talleres = (Taller.objects.raw( 
    "SELECT * FROM examen_taller ta "
    + " LEFT JOIN examen_revision re ON ta.id = re.taller_id "
    + " WHERE re.taller_id IS NULL" 
    )) 
    """
    
    return render(request,'lista_taller.html',{'Talleres_Mostrar':talleres})

#---------------------------------------------------------------------------

def dame_coches_nuevos(request):
    
    coches = (
        Coche.objects
        .filter(Q(anyo_lanzamiento__gte=2020)|Q(precio_base__lte=15000.00))
        .filter(revisionCoche__kilometraje__gt=50000)
        .all()
    )
    
    return render(request,'lista_coche.html',{'Coches_Mostrar':coches})

#---------------------------------------------------------------------------

def dame_mecanicos_experienca(request):
    
    mecanicos = (
        Mecanico.objects
        .filter(antiguedad__gt=5, revisionMecanico__resultado='AP')
        .all()
    )
    
    return render(request,'lista_mecanicos.html',{'Mecanicos_Mostrar':mecanicos})

#---------------------------------------------------------------------------

def dame_itvs_rechazadas(request):
    
    itvs = (
        Itv.objects
        .filter(resultado = 'R')
        .annotate(num_revisiones = Count("revisionItv"))
        .all()
    )
    
    
    return render(request, 'itvs_rechazadas.html',{'Itvs_Mostrar':itvs})

# Errores
def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)