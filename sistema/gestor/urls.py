from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('soporte/', views.soporte, name='soporte'),
    path('index/',views.proyectos, name='index'),
    
]   
