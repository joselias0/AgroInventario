from django.contrib import admin

from Modulos.distAvicola.models import *

# Register your models here.
admin.site.register(Tamaño)
admin.site.register(Producto)
admin.site.register(Lote)
admin.site.register(ventas)
admin.site.register(DetalleVentas)
admin.site.register(recursos)
admin.site.register(gastos_recursos)
admin.site.register(salud_gallinas)