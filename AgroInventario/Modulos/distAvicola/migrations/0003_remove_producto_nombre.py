# Generated by Django 5.0.3 on 2024-04-10 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distAvicola', '0002_gastos_recursos_productividad_recursos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='nombre',
        ),
    ]
