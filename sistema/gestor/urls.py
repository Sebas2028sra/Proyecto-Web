from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('soporte/', views.soporte, name='soporte'),
    path('index/', views.proyectos, name='index'),
    path('listado/', views.listado_proyectos, name='listado_proyectos'),
    path('agregar/', views.agregar_proyecto, name='agregar_proyecto'),
    path('actualizar/<int:id>/', views.actualizar_proyecto, name='actualizar_proyecto'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]