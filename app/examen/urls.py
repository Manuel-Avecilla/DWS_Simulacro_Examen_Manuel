from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('ultimo-voto/<int:id_movil>',views.dame_ultimo_voto, name='dame_ultimo_voto'),
    path('moviles-con-votos-malos/<int:id_usuario>',views.dame_moviles_malos, name='dame_moviles_malos'),
    path('usuarios-nunca-votaron/',views.dame_usuarios_nunca_votaron, name='dame_usuarios_nunca_votaron'),
    path('cuentas-bancarias/Caixa-Unicaja/<str:texto>',views.dame_cuentas_bancarias, name='dame_cuentas_bancarias'),
]