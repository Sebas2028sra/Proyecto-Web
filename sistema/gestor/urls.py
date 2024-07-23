from django.urls import path
from django.contrib.auth import views as auth_views
from .views import registro, login_view, logout_view, inicio, soporte, proyectos, listado_proyectos, agregar_proyecto, actualizar_proyecto, eliminar_proyecto

urlpatterns = [
    path('', inicio, name='inicio'),
    path('soporte/', soporte, name='soporte'),
    path('index/', proyectos, name='index'),
    path('listado/', listado_proyectos, name='listado_proyectos'),
    path('agregar/', agregar_proyecto, name='agregar_proyecto'),
    path('actualizar/<int:id>/', actualizar_proyecto, name='actualizar_proyecto'),
    path('eliminar/<int:id>/', eliminar_proyecto, name='eliminar_proyecto'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/registro/', registro, name='registro'),
]