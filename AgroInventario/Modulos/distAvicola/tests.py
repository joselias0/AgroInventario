from django.test import TestCase
from Modulos.distAvicola.views2 import *
from Modulos.distAvicola.views import *
from Modulos.distAvicola.models import *
from django.test import TestCase

class ModelTestCase(TestCase):
    def setUp(self):
        # Crear datos de prueba para los modelos
        self.tamaño = Tamaño.objects.create(nombre='Pequeño')
        self.producto = Producto.objects.create(cantidad=10, costo_produccion=100.0, tamaño=self.tamaño)
        self.lote = Lote.objects.create(produc=self.producto, cantidad=5, fecha_creacion='2024-04-20', fecha_vencimiento='2024-05-20', costo_produccion=50.0, precio_individual=20.0)
        self.venta = ventas.objects.create(cantidad=3, precio_final=25.0, fecha='2024-04-22')
        self.detalle_venta = DetalleVentas.objects.create(venta=self.venta)
        self.recurso = recursos.objects.create(nombre_recurso='Maíz', descripcion='Maíz para alimentar a las gallinas', cantidad_disponible=100)
        self.gasto_recurso = gastos_recursos.objects.create(id_recurso=self.recurso, precio=10.0, fecha='2024-04-22', cantidad_agregada=50)
        self.salud_gallina = salud_gallinas.objects.create(tipo_accion='Vacunación', fecha='2024-04-22', id_recurso=self.recurso, comentarios='Vacuna contra la gripe aviar', cantidad_recurso_usado=10)

    def test_model_creation(self):
        # Prueba para verificar que los modelos se crearon correctamente
        self.assertEqual(Tamaño.objects.count(), 1)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Lote.objects.count(), 1)
        self.assertEqual(ventas.objects.count(), 1)
        self.assertEqual(DetalleVentas.objects.count(), 1)
        self.assertEqual(recursos.objects.count(), 1)
        self.assertEqual(gastos_recursos.objects.count(), 1)
        self.assertEqual(salud_gallinas.objects.count(), 1)

    def test_related_models(self):
        # Prueba para verificar las relaciones entre modelos
        self.assertEqual(self.producto.tamaño, self.tamaño)
        self.assertEqual(self.lote.produc, self.producto)
        self.assertEqual(self.detalle_venta.venta, self.venta)
        self.assertIn(self.lote, self.detalle_venta.lotes.all())
        self.assertEqual(self.gasto_recurso.id_recurso, self.recurso)
        self.assertEqual(self.salud_gallina.id_recurso, self.recurso)

from django.urls import reverse, resolve
from Modulos.distAvicola.views2 import *
from django.test import SimpleTestCase
from Modulos.distAvicola.views import *
from Modulos.distAvicola.models import *

class UrlTests(SimpleTestCase):
    def test_url_huevos_resolves(self):
        url = reverse('huevos')
        self.assertEqual(resolve(url).func, huevos)

    def test_url_salir_resolves(self):
        url = reverse('salir')
        self.assertEqual(resolve(url).func, salir)

    def test_url_ventas_resolves(self):
        url = reverse('ventas')
        self.assertEqual(resolve(url).func, venta)

    def test_url_contabilidad_resolves(self):
        url = reverse('contabilidad')
        self.assertEqual(resolve(url).func, contabilidad)

    def test_url_generar_pdf_vp_resolves(self):
        url = reverse('generar_pdf_vp')
        self.assertEqual(resolve(url).func, generar_pdf_vp)

    def test_url_pag_borrar_prod_resolves(self):
        url = reverse('pag_borrar_prod', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, pag_borrar_prod)

    def test_url_pag_borrar_lot_resolves(self):
        url = reverse('pag_borrar_lot', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, pag_borrar_lot)

    def test_url_pag_add_tamano_resolves(self):
        url = reverse('pag_add_tamano')
        self.assertEqual(resolve(url).func, pag_add_tamano)

    def test_url_pag_add_inventario_resolves(self):
        url = reverse('pag_add_inventario', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, pag_add_inventario)

    def test_url_add_tamano_resolves(self):
        url = reverse('add_tamano')
        self.assertEqual(resolve(url).func, add_tamano)

    def test_url_borrar_tamano_resolves(self):
        url = reverse('borrar_tamano', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, borrar_tamano)

    def test_url_edit_tamano_resolves(self):
        url = reverse('edit_tamano', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, edit_tamano)

    def test_url_ver_lotes_resolves(self):
        url = reverse('ver-lotes', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, ver_lotes)

    def test_url_edit_lote_resolves(self):
        url = reverse('edit_lote', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, edit_lote)

    def test_url_borrar_lote_resolves(self):
        url = reverse('borrar_lote', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, borrar_lote)

    def test_url_pag_add_venta_resolves(self):
        url = reverse('pag_add_venta')
        self.assertEqual(resolve(url).func, pag_add_venta)

    def test_url_add_venta_resolves(self):
        url = reverse('add_venta')
        self.assertEqual(resolve(url).func, add_venta)

    def test_url_r_devolucion_resolves(self):
        url = reverse('r_devolucion', args=[1])  # Reemplaza 1 con el ID adecuado
        self.assertEqual(resolve(url).func, r_devolucion)

from django.test import TestCase, Client
from django.urls import reverse, resolve
from Modulos.distAvicola.views2 import *
from django.test import SimpleTestCase
from Modulos.distAvicola.views import *
from Modulos.distAvicola.models import *
from django.test import TestCase

class ViewTests(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.client = Client()

    def test_generar_pdf_vp(self):
        # Prueba para la vista generar_pdf_vp
        response = self.client.get(reverse('generar_pdf_vp'))
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_pag_add_tamano(self):
        # Prueba para la vista pag_add_tamano
        response = self.client.get(reverse('pag_add_tamano'))
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_pag_add_inventario(self):
        # Prueba para la vista pag_add_inventario
        response = self.client.get(reverse('pag_add_inventario', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    # Continúa con pruebas similares para las demás vistas...

    def test_r_devolucion(self):
        # Prueba para la vista r_devolucion
        response = self.client.get(reverse('r_devolucion', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado
    
    def test_ver_lotes(self):
        # Prueba para la vista ver_lotes
        response = self.client.get(reverse('ver_lotes', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_borrar_lote(self):
        # Prueba para la vista borrar_lote
        response = self.client.get(reverse('borrar_lote', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_pag_borrar_prod(self):
        # Prueba para la vista pag_borrar_prod
        response = self.client.get(reverse('pag_borrar_prod', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_pag_borrar_lot(self):
        # Prueba para la vista pag_borrar_lot
        response = self.client.get(reverse('pag_borrar_lot', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_edit_lote(self):
        # Prueba para la vista edit_lote
        response = self.client.get(reverse('edit_lote', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_add_tamano(self):
        # Prueba para la vista add_tamano
        response = self.client.post(reverse('add_tamano'), {'precio': '10.00', 'tamaño': 1})  # Reemplaza '10.00' y 1 con los valores adecuados
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_borrar_tamano(self):
        # Prueba para la vista borrar_tamano
        response = self.client.get(reverse('borrar_tamano', args=[1]))  # Reemplaza 1 con el ID adecuado
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_edit_tamano(self):
        # Prueba para la vista edit_tamano
        response = self.client.post(reverse('edit_tamano', args=[1]), {'precio': '10.00', 'tamaño': 1})  # Reemplaza 1 y '10.00' con los valores adecuados
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_pag_add_venta(self):
        # Prueba para la vista pag_add_venta
        response = self.client.get(reverse('pag_add_venta'))
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado

    def test_add_venta(self):
        # Prueba para la vista add_venta
        response = self.client.post(reverse('add_venta'), {'cantidad': 10, 'producto': 1, 'fecha': '2024-04-24'})  # Reemplaza 10, 1 y '2024-04-24' con los valores adecuados
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar la respuesta de la vista según lo esperado