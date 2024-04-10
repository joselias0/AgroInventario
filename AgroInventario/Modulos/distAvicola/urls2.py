from django.urls import path 
from .views2 import *
from .views import *

urlpatterns = [
    path('huevos/',huevos, name='huevos'),
    path('salir/', salir, name='salir' ),
    path('ventas/',venta, name='ventas'),
    path('contabilidad/',contabilidad, name='contabilidad'),
    path('generar_pdf_vp/',generar_pdf_vp, name='generar_pdf_vp'), 
    path('pag_add_tamaño/', pag_add_tamaño,name='pag_add_tamaño'),
    path('pag_add_inventario/<int:id1>/', pag_add_inventario, name='pag_add_inventario'),
    path('add_tamano/', add_tamano, name='add_tamano'),
    path('borrar_tamano/<int:id>/', borrar_tamano, name='borrar_tamano'),
    path('edit_tamano/<int:id>/', edit_tamano, name='edit_tamano'),
]