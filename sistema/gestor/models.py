from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, verbose_name='ID Usuario')
    nombre_usuario = models.CharField(max_length=255, unique=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_usuario + ' - ' + self.correo + ' - ' + self.contrasena + ' - ' + str(self.id_usuario)

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True, verbose_name='ID Estado')
    descripcion_estado = models.CharField(max_length=50)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion_estado

class Prioridad(models.Model):
    id_prioridad = models.AutoField(primary_key=True, verbose_name='ID Prioridad')
    descripcion_prioridad = models.CharField(max_length=50)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion_prioridad

class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True, verbose_name='ID Proyecto')
    nombre_proyecto = models.CharField(max_length=255)
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    id_prioridad = models.ForeignKey(Prioridad, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField(default=timezone.now() + timedelta(days=30))
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_proyecto
