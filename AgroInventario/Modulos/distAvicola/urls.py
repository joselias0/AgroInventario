from django.urls import path 
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('',index, name='index'),
    path('salir/', salir, name='salir' ),
    path('huevos/',huevos, name='huevos'),
    path('contabilidad/',contabilidad, name='contabilidad'),
    path('cuidado/',cuidado, name='cuidado'),
    path('recurso/',recurso, name='recurso'),
    path('recursos/gasto/<int:id_recurso>',agregarGasto, name='gasto'),
    path('recursos/adicion', adicion, name='adicion'),
    path('recursos/editarRecurso/<int:id>', editarRecurso, name='editar_recurso'),
    path('eliminarRecurso/<int:id>', eliminarRecurso,name='eliminarRecurso'),
    path('recursos/',recursos, name='recursos'),
    path('cuidado/',cuidado, name='cuidado')
]

