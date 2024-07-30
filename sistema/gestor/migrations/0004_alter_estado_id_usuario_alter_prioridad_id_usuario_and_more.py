# Generated by Django 5.0.6 on 2024-07-29 07:48

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0003_alter_estado_id_usuario_alter_prioridad_id_usuario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='id_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prioridad',
            name='id_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_vencimiento',
            field=models.DateField(default=datetime.datetime(2024, 8, 28, 7, 48, 2, 676096, tzinfo=datetime.timezone.utc)),
        ),
    ]