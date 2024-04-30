from django.urls import path 
from .views2 import *
from .views import *

urlpatterns = [
    path('huevos/',huevos, name='huevos'),
    path('salir/', salir, name='salir' ),
    path('ventas/',venta, name='ventas'),
    path('contabilidad/',contabilidad, name='contabilidad'),
    path('generar_pdf_vp/',generar_pdf_vp, name='generar_pdf_vp'),
    path('pag_borrar_prod/<int:id>/', pag_borrar_prod, name='pag_borrar_prod'),
    path('pag_borrar_lot/<int:id>/', pag_borrar_lot, name='pag_borrar_lot'), 
    path('pag_add_tamano/', pag_add_tamano,name='pag_add_tamano'),
    path('pag_add_inventario/<int:id1>/', pag_add_inventario, name='pag_add_inventario'),
    path('add_tamano/', add_tamano, name='add_tamano'),
    path('borrar_tamano/<int:id>/', borrar_tamano, name='borrar_tamano'),
    path('edit_tamano/<int:id>/', edit_tamano, name='edit_tamano'),
    path('ver-lotes/<int:id>/', ver_lotes, name='ver-lotes'),
    path('edit_lote/<int:id>/', edit_lote, name='edit_lote'),
    path('borrar_lote/<int:id>/', borrar_lote, name='borrar_lote'),
    path('pag_add_venta/', pag_add_venta,name='pag_add_venta'),
    path('add_venta/', add_venta, name='add_venta'),
    path('r_devolucion/<int:id>', r_devolucion, name='r_devolucion'),
]