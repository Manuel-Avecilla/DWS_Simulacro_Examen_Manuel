from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('coches/ultima-revision/<int:id_coche>/', views.dame_ultima_revision, name='dame_ultima_revision'),
    path('coches/fallos-graves/', views.dame_coche_revision_grave, name='dame_coche_revision_grave'),
    path('talleres/sin-revisiones/', views.dame_talleres_sin_revision, name='dame_talleres_sin_revision'),
    path('coches/filtrar/',views.dame_coches_nuevos, name='dame_coches_nuevos'),
    path('mecanicos/experiencia/',views.dame_mecanicos_experienca, name='dame_mecanicos_experienca'),
    path('itvs/rechazadas/',views.dame_itvs_rechazadas, name='dame_itvs_rechazadas')
]