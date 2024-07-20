from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('administrarcion_malla/', views.administracion_malla, name='administracion_malla'),
    path('list_malla/', views.list_malla, name='list_malla'),
    path('nueva_malla/', views.nueva_malla, name='nueva_malla'),
    path('confirmar_malla/', views.confirmar_malla, name='confirmar_malla'),
    path('editar_malla/<int:malla_id>/', views.editar_malla, name='editar_malla'),
    path('importar/', views.importar_datos_periodo_historico, name='importar_datos'),
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    path('list_periodo/', views.list_periodos_historicos, name='list_periodo'),
    path('administracion_periodo/', views.administracion_periodo, name='administracion_periodo'),
    path('editar_periodo/<int:periodo_id>/', views.editar_datos_periodo_historico, name='editar_periodo'),
    path('eliminar_periodo/<int:periodo_id>/', views.eliminar_datos_periodo_historico, name='eliminar_periodo'),
]