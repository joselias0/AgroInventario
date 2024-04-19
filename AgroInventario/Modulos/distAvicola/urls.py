from django.urls import path 
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('',index, name='index'),
    path('salir/', salir, name='salir' ),
<<<<<<< HEAD
    path('huevos/',huevos, name='huevos'),
    path('ventas/',ventas, name='ventas'),
    path('recurso/',recurso, name='recurso'),
    path('contabilidad/',contabilidad, name='contabilidad'),
    path('cuidado/',cuidado, name='cuidado'),
    path('recursos/gasto/<int:id_recurso>',agregarGasto, name='gasto'),
    path('recursos/adicion', adicion, name='adicion'),
    path('recursos/editarRecurso/<int:id>', editarRecurso, name='editar_recurso'),
    path('eliminarRecurso/<int:id>', eliminarRecurso,name='eliminarRecurso'),

=======
    path('recursos/',recursos, name='recursos'),
    path('cuidado/',cuidado, name='cuidado')
>>>>>>> 56afc465aff3921e18c22fac0a2fce58e76e9ce6
]

