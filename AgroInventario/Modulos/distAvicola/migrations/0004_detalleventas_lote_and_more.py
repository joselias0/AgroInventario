# Generated by Django 4.0.10 on 2024-04-25 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distAvicola', '0003_remove_producto_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleVentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateField()),
                ('fecha_vencimiento', models.DateField(null=True)),
                ('costo_produccion', models.FloatField()),
                ('precio_individual', models.FloatField()),
            ],
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='precio',
            new_name='costo_produccion',
        ),
        migrations.RemoveField(
            model_name='ventas',
            name='producto_id',
        ),
        migrations.AlterField(
            model_name='producto',
            name='tamaño',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.tamaño'),
        ),
        migrations.DeleteModel(
            name='productividad',
        ),
        migrations.AddField(
            model_name='lote',
            name='produc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='distAvicola.producto'),
        ),
        migrations.AddField(
            model_name='detalleventas',
            name='lotes',
            field=models.ManyToManyField(to='distAvicola.lote'),
        ),
        migrations.AddField(
            model_name='detalleventas',
            name='venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='distAvicola.ventas'),
        ),
    ]
