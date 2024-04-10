from django.db import models


class Tamaño(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    
class Producto(models.Model):
    id = models.AutoField(primary_key=True)  
    cantidad = models.IntegerField()
    precio = models.FloatField()
    tamaño = models.ForeignKey(Tamaño, to_field='id', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
    
class productividad(models.Model):
    id = models.AutoField(primary_key=True) 
    fecha = models.DateField()
    cantidad_agregada = models.IntegerField()
    id_producto = models.ForeignKey(Producto, to_field='id', on_delete=models.SET_NULL, null=True)


class ventas(models.Model):
    id = models.AutoField(primary_key=True)
    producto_id = models.ForeignKey(Producto, to_field='id', on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_final = models.FloatField()
    fecha = models.DateField()
    

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


    




