from django.db import models

class Tamaño(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=45)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)  
    cantidad = models.IntegerField()
    costo_produccion = models.FloatField()
    tamaño = models.OneToOneField(Tamaño, on_delete=models.SET_NULL, null=True)

class Lote(models.Model):
    id = models.AutoField(primary_key=True)
    produc = models.ForeignKey(Producto,to_field="id",  on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(default=0)
    fecha_creacion = models.DateField()
    fecha_vencimiento =  models.DateField(null=True)
    costo_produccion = models.FloatField()
    precio_individual = models.FloatField()

class ventas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    cantidad = models.IntegerField()
    precio_final = models.FloatField()
    fecha = models.DateField()

class DetalleVentas(models.Model):
    venta = models.ForeignKey(ventas, to_field="id" , on_delete=models.SET_NULL, null=True)
    lotes = models.ManyToManyField(Lote)
    
class recursos(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre_recurso = models.CharField(max_length=45)
    descripcion = models.TextField()
    cantidad_disponible = models.IntegerField()

class gastos_recursos(models.Model):
    id = models.AutoField(primary_key=True)
    id_recurso = models.ForeignKey(recursos, to_field='id', on_delete=models.SET_NULL, null=True)
    precio = models.FloatField()
    fecha = models.DateField()
    cantidad_agregada = models.IntegerField()

class salud_gallinas(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_accion = models.CharField(max_length=45)
    fecha = models.DateField()
    id_recurso = models.ForeignKey(recursos, to_field='id', on_delete=models.SET_NULL, null=True)
    comentarios = models.TextField()
    cantidad_recurso_usado = models.IntegerField()


    




