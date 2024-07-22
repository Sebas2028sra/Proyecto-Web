from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Estado, Prioridad, Proyecto

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')

def inicio(request):
    return render(request, 'paginas/inicio.html')

def soporte(request):
    return render(request, 'paginas/soporte.html')

@login_required(login_url='/accounts/login/')
def proyectos(request):
    proyectos = Proyecto.objects.filter(id_usuario=request.user)
    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    return render(request, 'proyectos/index.html', {
        'proyectos': proyectos,
        'estados': estados,
        'prioridades': prioridades,
    })

@login_required(login_url='/accounts/login/')
def listado_proyectos(request):
    proyectos = Proyecto.objects.filter(id_usuario=request.user)
    estados = Estado.objects.all()
    prioridades = Prioridad.objects.all()
    return render(request, 'listado_proyectos.html', {
        'proyectos': proyectos,
        'estados': estados,
        'prioridades': prioridades,
    })

@login_required(login_url='/accounts/login/')
def agregar_proyecto(request):
    if request.method == 'POST':
        nombre_proyecto = request.POST['nombre_proyecto']
        id_estado = request.POST['id_estado']
        id_prioridad = request.POST['id_prioridad']
        fecha_vencimiento = request.POST['fecha_vencimiento']
        usuario = request.user
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

@login_required(login_url='/accounts/login/')
def actualizar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id, id_usuario=request.user)
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

@login_required(login_url='/accounts/login/')
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id, id_usuario=request.user)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('index')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto})