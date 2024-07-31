# Generated by Django 5.0.6 on 2024-07-31 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0006_alter_proyecto_fecha_vencimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_vencimiento',
            field=models.DateField(default=datetime.datetime(2024, 8, 30, 6, 38, 37, 708414, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='responsable',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
