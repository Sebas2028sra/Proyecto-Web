from django.shortcuts import render
from django.http import HttpResponse    
from .models import Proyecto

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')

def soporte(request):
    return render(request, 'paginas/soporte.html')

def proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/index.html', {'proyectos': proyectos})