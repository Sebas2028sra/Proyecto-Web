from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Estado, Prioridad, Proyecto
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages

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
        responsable = request.POST['responsable']
        id_estado = request.POST['id_estado']
        id_prioridad = request.POST['id_prioridad']
        fecha_vencimiento = request.POST['fecha_vencimiento']
        porcentaje = int(request.POST['porcentaje'])  # Obtenemos el porcentaje
        usuario = request.user

        estado = get_object_or_404(Estado, Q(id_estado=id_estado) & (Q(id_usuario=usuario) | Q(id_usuario=None)))
        prioridad = get_object_or_404(Prioridad, Q(id_prioridad=id_prioridad) & (Q(id_usuario=usuario) | Q(id_usuario=None)))

        # Validar el correo electrónico del responsable si no está vacío
        if responsable:
            try:
                validate_email(responsable)
            except ValidationError:
                messages.error(request, 'Por favor, agregue una dirección de correo electrónico válida o no agregue ningún valor al campo.')
                return render(request, 'proyectos/agregar.html', {
                    'estados': Estado.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None)),
                    'prioridades': Prioridad.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None)),
                })

        nuevo_proyecto = Proyecto(
            nombre_proyecto=nombre_proyecto,
            responsable=responsable,
            id_estado=estado,
            id_prioridad=prioridad,
            fecha_vencimiento=fecha_vencimiento,
            porcentaje=porcentaje,  # Guardamos el porcentaje
            id_usuario=usuario
        )

        nuevo_proyecto.save()

        # Enviar correo electrónico al responsable si se ingresó un correo válido
        if responsable:
            send_mail(
                'Nuevo Proyecto Asignado',
                f'Hola, {responsable}. Se te ha asignado el proyecto "{nombre_proyecto}".\n\n'
                f'Detalles del proyecto:\n'
                f'- Estado: {estado.descripcion_estado}\n'
                f'- Prioridad: {prioridad.descripcion_prioridad}\n'
                f'- Fecha de Vencimiento: {fecha_vencimiento}\n',
                settings.DEFAULT_FROM_EMAIL,
                [responsable],
                fail_silently=False,
            )

        return redirect('index')
    else:
        estados = Estado.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None))
        prioridades = Prioridad.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None))
        return render(request, 'proyectos/agregar.html', {'estados': estados, 'prioridades': prioridades})


@login_required(login_url='/accounts/login/')
def actualizar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id, id_usuario=request.user)
    if request.method == 'POST':
        proyecto.nombre_proyecto = request.POST['nombre_proyecto']
        proyecto.responsable = request.POST['responsable']
        proyecto.id_estado = get_object_or_404(Estado, Q(id_estado=request.POST['id_estado']) & (Q(id_usuario=request.user) | Q(id_usuario=None)))
        proyecto.id_prioridad = get_object_or_404(Prioridad, Q(id_prioridad=request.POST['id_prioridad']) & (Q(id_usuario=request.user) | Q(id_usuario=None)))
        proyecto.fecha_vencimiento = request.POST['fecha_vencimiento']
        proyecto.porcentaje = int(request.POST['porcentaje'])  # Actualizamos el porcentaje
        proyecto.save()
        return redirect('index')
    else:
        estados = Estado.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None))
        prioridades = Prioridad.objects.filter(Q(id_usuario=request.user) | Q(id_usuario=None))
        return render(request, 'proyectos/editar.html', {'proyecto': proyecto, 'estados': estados, 'prioridades': prioridades})

@login_required(login_url='/accounts/login/')
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id, id_usuario=request.user)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('index')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto})

@login_required(login_url='/accounts/login/')
def custom_estado(request):
    if request.method == 'POST':
        descripcion_estado = request.POST['descripcion_estado']
        estado = Estado(descripcion_estado=descripcion_estado, id_usuario=request.user)
        estado.save()
        return redirect('index')
    else:
        estados_personalizados = Estado.objects.filter(id_usuario=request.user)
        return render(request, 'proyectos/custom_estado.html', {'estados_personalizados': estados_personalizados})

@login_required(login_url='/accounts/login/')
def eliminar_estado(request, id):
    estado = get_object_or_404(Estado, id_estado=id, id_usuario=request.user)
    if request.method == 'POST':
        estado.delete()
        return redirect('custom_estado')
    return render(request, 'proyectos/eliminar_estado.html', {'estado': estado})

@login_required(login_url='/accounts/login/')
def custom_prioridad(request):
    if request.method == 'POST':
        descripcion_prioridad = request.POST['descripcion_prioridad']
        prioridad = Prioridad(descripcion_prioridad=descripcion_prioridad, id_usuario=request.user)
        prioridad.save()
        return redirect('index')
    else:
        prioridades_personalizadas = Prioridad.objects.filter(id_usuario=request.user)
        return render(request, 'proyectos/custom_prioridad.html', {'prioridades_personalizadas': prioridades_personalizadas})

@login_required(login_url='/accounts/login/')
def eliminar_prioridad(request, id):
    prioridad = get_object_or_404(Prioridad, id_prioridad=id, id_usuario=request.user)
    if request.method == 'POST':
        prioridad.delete()
        return redirect('custom_prioridad')
    return render(request, 'proyectos/eliminar_prioridad.html', {'prioridad': prioridad})


from django.core.mail import send_mail
from django.conf import settings

def soporte(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        mensaje = request.POST['mensaje']
        asunto = f"Reporte de Soporte de {nombre}"
        mensaje_completo = f"Nombre: {nombre}\nCorreo Electrónico: {correo}\n\nMensaje:\n{mensaje}"
        
        # Enviar el correo
        send_mail(
            asunto, 
            mensaje_completo, 
            settings.DEFAULT_FROM_EMAIL, 
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
        return render(request, 'paginas/soporte.html', {'mensaje_enviado': True})
    return render(request, 'paginas/soporte.html')