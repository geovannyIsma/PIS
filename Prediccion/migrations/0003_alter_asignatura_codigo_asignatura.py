# Generated by Django 5.0.6 on 2024-07-09 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prediccion', '0002_remove_ciclo_cantidad_asignaturas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='codigo_asignatura',
            field=models.CharField(max_length=50, verbose_name='Código de Asignatura'),
        ),
    ]
