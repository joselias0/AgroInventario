# Generated by Django 5.0.3 on 2024-04-07 04:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distAvicola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='gastos_recursos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('precio', models.FloatField()),
                ('fecha', models.DateField()),
                ('cantidad_agregada', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='productividad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('cantidad_agregada', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='recursos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_recurso', models.CharField(max_length=45)),
                ('descripcion', models.TextField()),
                ('cantidad_disponible', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='salud_gallinas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_accion', models.CharField(max_length=45)),
                ('fecha', models.DateField()),
                ('comentarios', models.TextField()),
                ('cantidad_recurso_usado', models.IntegerField()),
                ('id_recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.recursos')),
            ],
        ),
        migrations.CreateModel(
            name='ventas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio_final', models.FloatField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Gasto',
        ),
        migrations.AlterField(
            model_name='producto',
            name='tamaño',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.tamaño'),
        ),
        migrations.AddField(
            model_name='productividad',
            name='id_producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.producto'),
        ),
        migrations.AddField(
            model_name='gastos_recursos',
            name='id_recurso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.recursos'),
        ),
        migrations.AddField(
            model_name='ventas',
            name='producto_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.producto'),
        ),
        migrations.DeleteModel(
            name='Venta',
        ),
    ]
