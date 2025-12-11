# ============================================================
# region Importaciones
# ============================================================

from django.urls import path
from . import views
from .views import MiLoginView

# endregion
# ============================================================


urlpatterns = [
    
    #---HOME---
    path('',views.home, name='home'),
    
    
    #---REGISTRO-LOGIN---
    
    # Registro
    path('registro/usuario',views.registrar_usuario,name='registrar_usuario'),
    
    # Login
    path('accounts/login/', MiLoginView.as_view(), name='login'),


    #---Usuario---
    #---------Detalles-Lista---------
    path('usuario/listar', views.usuarios_listar, name='usuarios_listar'),
    path('usuario/<int:id_usuario>', views.dame_usuario, name='dame_usuario'),
    
    #---Organizador---
    #---------Detalles-Lista---------
    path('organizador/listar', views.organizadores_listar, name='organizadores_listar'),
    path('organizador/<int:id_organizador>', views.dame_organizador, name='dame_organizador'),
    
    #----EVENTO-----
    
    #---------Detalles-Lista---------
    path('evento/listar', views.eventos_listar, name='eventos_listar'),
    path('evento/<int:id_evento>', views.dame_evento, name='dame_evento'),
    
    #--------------CRUD--------------
    path('evento/crear/',views.evento_create, name='evento_create'),
    path('evento/buscar/avanzado/',views.evento_buscar_avanzado, name='evento_buscar_avanzado'),
    path('evento/editar/<int:id_evento>', views.evento_editar, name="evento_editar"),
    path('evento/eliminar/<int:id_evento>', views.evento_eliminar, name="evento_eliminar"),
    
    #---CRUD---
]