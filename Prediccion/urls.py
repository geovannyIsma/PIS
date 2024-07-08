from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('administrarcion_malla/', views.administracion_malla, name='administracion_malla'),
    path('list_malla/', views.list_malla, name='list_malla'),
]