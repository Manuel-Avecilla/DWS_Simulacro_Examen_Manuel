from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('animal/<int:id_animal>',views.dame_animal, name='dame_animal'),
    path('ultima-revision/<int:id_animal>/', views.dame_revision, name='dame_revision'),
    path('animales-con-revisiones/',views.dame_alimales_revisiones, name='dame_alimales_revisiones'),
    path('tipos-sin-animales/', views.dame_tipo_sin_animales, name="dame_tipo_sin_animales"),
    path('alertas-pendiente-2025/', views.dame_alerta_pendiente_2025, name ="dame_alerta_pendiente_2025")
]