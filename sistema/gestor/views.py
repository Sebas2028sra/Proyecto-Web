from django.shortcuts import render
from django.http import HttpResponse    

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')

def soporte(request):
    return render(request, 'paginas/soporte.html')

def proyectos(request):
    return render(request, 'proyectos/index.html')