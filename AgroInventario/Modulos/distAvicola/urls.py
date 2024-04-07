from django.urls import path 
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('',index, name='index'),
    path('salir/', salir, name='salir' ),
    path('huevos/',huevos, name='huevos'),
    path('ventas/',ventas, name='ventas'),
    path('recursos/',recursos, name='recursos'),
    path('contabilidad/',contabilidad, name='contabilidad'),
    path('cuidado/',cuidado, name='cuidado'),
]

