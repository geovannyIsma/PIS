# Generated by Django 5.0.6 on 2024-07-25 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prediccion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrador'), ('consultor', 'Consultor')], default='consultor', max_length=50),
        ),
    ]