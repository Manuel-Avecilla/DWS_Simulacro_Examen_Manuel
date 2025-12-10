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
    
    #---Tecnico---
    #---------Detalles-Lista---------
    path('tecnico/listar', views.tecnicos_listar, name='tecnicos_listar'),
    path('tecnico/<int:id_tecnico>', views.dame_tecnico, name='dame_tecnico'),
    
    
    
    #---CRUD---
]