from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('administrarcion_malla/', views.administracion_malla, name='administracion_malla'),
    path('list_malla/', views.list_malla, name='list_malla'),
    path('nueva_malla/', views.nueva_malla, name='nueva_malla'),
    path('confirmar_malla/', views.confirmar_malla, name='confirmar_malla'),
    path('editar_malla/<int:malla_id>/', views.editar_malla, name='editar_malla'),
    path('importar/', views.importar_datos, name='importar_datos'),
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
]