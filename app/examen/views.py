from django.shortcuts import render
from .models import *
from django.db.models import Q , Prefetch, Avg, Max, Min
from django.views.defaults import page_not_found

# Create your views here.

def index(request):
    return render(request, 'index.html')

# El último voto que se realizó en un modelo principal en concreto, y mostrar el
# comentario, la votación e información del usuario o cliente que lo realizó:
def dame_ultimo_voto(request, id_movil):
    
    voto = (
        Votar.objects
        .select_related("usuario","movil")
        .filter(movil__id = id_movil) # Obtiene el movil con el ID especificado
        .order_by("-fecha_envio")[:1].get()
    )

    """
    voto = (Votar.objects.raw(
    "SELECT * FROM examen_votar vo "
    + " JOIN examen_usuario user ON user.id = vo.usuario_id "
    + " JOIN examen_movil mo ON mo.id = vo.movil_id "
    + " WHERE vo.movil_id = %s " 
    + " ORDER BY vo.fecha_envio DESC "
    + " LIMIT 1 " 
    ,[id_movil] 
    )[0])
    """
    
    return render(request,'Voto.html',{'Voto_Mostrar':voto})


# Todos los modelos principales que tengan votos con una puntuación numérica
# menor a 3 y que realizó un usuario o cliente en concreto:
def dame_moviles_malos(request, id_usuario):
    
    moviles = (
        Movil.objects
        .prefetch_related("votos")
        .filter(votar_movil__usuario_id = id_usuario)
    )
    moviles.filter(Q(votar_movil__puntuacion=2)|Q(votar_movil__puntuacion=1)|Q(votar_movil__puntuacion=0))
    moviles.all()
    
    """
    moviles = (Movil.objects.raw(
    "SELECT * FROM examen_movil mo "
    + " JOIN examen_votar vo ON mo.id = vo.movil_id "
    + " WHERE vo.usuario_id = %s AND vo.puntuacion < 3"
    ,[id_usuario] 
    ))
    """
    
    return render(request,'Lista_Moviles.html',{'Moviles_Mostrar':moviles})

# Todos los usuarios o clientes que no han votado nunca y mostrar información sobre
# estos usuarios y clientes al completo:
def dame_usuarios_nunca_votaron(request):
    
    usuarios = (
        Usuario.objects
        .filter(votar_usuario = None)
    )
    usuarios.all()
    
    """
    usuarios = (Usuario.objects.raw(
    "SELECT * FROM examen_usuario user "
    + " LEFT JOIN examen_votar vo ON vo.usuario_id = user.id "
    + " WHERE vo.usuario_id IS NULL "
    ))
    """
    
    return render(request,'Lista_Usuarios.html',{'Usuarios_Mostrar':usuarios})

# Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el
# propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”:

def dame_cuentas_bancarias(request, texto):
    
    cuentas = (
        CuentaBancaria.objects
        .select_related("usuario")
        .filter(Q(banco = "CX")|Q(banco = "UN"))
        .filter(usuario__nombre_usuario__contains=texto)
    )
    cuentas.all()
    
    return render(request,'Lista_Cuentas_Bancarias.html',{'Cuentas_Bancarias_Mostrar':cuentas})


# Errores
def mi_error_404(request,exception=None):
    return render(request,'error/404.html',None,None,404)

def mi_error_403(request,exception=None):
    return render(request,'error/403.html',None,None,403)

def mi_error_400(request,exception=None):
    return render(request,'error/400.html',None,None,400)

def mi_error_500(request,exception=None):
    return render(request,'error/500.html',None,None,500)