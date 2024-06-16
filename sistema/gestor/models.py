from django.db import models

# Create your models here.
class Proyecto(models.Model):
    id = models.AutoField(primary_key=True , verbose_name='ID')
    tarea = models.CharField(max_length=100, verbose_name='Tarea')
    estado = models.CharField(max_length=100, verbose_name='Estado')
    prioridad = models.CharField(max_length=100, verbose_name='Prioridad')
    fecha_entrega = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Entrega')

def __str__(self):
    fila = str(self.tarea) + " - " + str(self.estado)+" - "+str(self.prioridad)
    return fila



