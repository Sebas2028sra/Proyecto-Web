from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Usuario, Estado, Prioridad, Proyecto

def inicio(request):
    return render(request, 'paginas/inicio.html')

def soporte(request):
    return render(request, 'paginas/soporte.html')

def proyectos(request):
    proyectos = Proyecto.objects.all()
    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    return render(request, 'proyectos/index.html', {
        'proyectos': proyectos,
        'estados': estados,
        'prioridades': prioridades,
    })

def listado_proyectos(request):
    proyectos = Proyecto.objects.all()
    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'listado_proyectos.html', {
        'proyectos': proyectos,
        'estados': estados,
        'prioridades': prioridades,
        'usuarios': usuarios
    })

def agregar_proyecto(request):
    if request.method == 'POST':
        nombre_proyecto = request.POST['nombre_proyecto']
        id_estado = request.POST['id_estado']
        id_prioridad = request.POST['id_prioridad']
        fecha_vencimiento = request.POST['fecha_vencimiento']
        usuario = Usuario.objects.first() 
        estado = Estado.objects.get(id_estado=id_estado)
        prioridad = Prioridad.objects.get(id_prioridad=id_prioridad)
        nuevo_proyecto = Proyecto(
            nombre_proyecto=nombre_proyecto,
            id_estado=estado,
            id_prioridad=prioridad,
            fecha_vencimiento=fecha_vencimiento,
            id_usuario=usuario
        )
        nuevo_proyecto.save()
        return redirect('index')
    else:
        estados = Estado.objects.all()
        prioridades = Prioridad.objects.all()
        return render(request, 'proyectos/agregar.html', {
            'estados': estados,
            'prioridades': prioridades,
        })

def actualizar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id)
    if request.method == 'POST':
        proyecto.nombre_proyecto = request.POST['nombre_proyecto']
        proyecto.id_estado = Estado.objects.get(id_estado=request.POST['id_estado'])
        proyecto.id_prioridad = Prioridad.objects.get(id_prioridad=request.POST['id_prioridad'])
        proyecto.fecha_vencimiento = request.POST['fecha_vencimiento']
        proyecto.save()
        return redirect('index')
    else:
        estados = Estado.objects.all()
        prioridades = Prioridad.objects.all()
        return render(request, 'proyectos/editar.html', {
            'proyecto': proyecto,
            'estados': estados,
            'prioridades': prioridades,
        })

def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('index')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto})