from django.urls import path
from . import views
from .views import leer_feedback

urlpatterns = [
    path('home/', views.dashboard_view, name='home'),
    path('administrarcion_malla/', views.administracion_malla, name='administracion_malla'),
    path('list_malla/', views.list_malla, name='list_malla'),
    path('nueva_malla/', views.nueva_malla, name='nueva_malla'),
    path('confirmar_malla/', views.confirmar_malla, name='confirmar_malla'),
    path('editar_malla/<int:malla_id>/', views.editar_malla, name='editar_malla'),
    path('eliminar_malla/<int:malla_id>/', views.eliminar_malla, name='eliminar_malla'),
    path('list_periodo/', views.list_periodos_historicos, name='list_periodo'),
    path('administracion_periodo/', views.administracion_periodo, name='administracion_periodo'),
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    path('importar_datos/', views.importar_datos_periodo_historico, name='importar_datos'),
    path('editar_periodo/<int:periodo_id>/', views.editar_datos_periodo_historico, name='editar_periodo'),
    path('eliminar_periodo/<int:periodo_id>/', views.eliminar_datos_periodo_historico, name='eliminar_periodo'),
    path('modelo_matematico/', views.modelo_matematico, name='modelo_matematico'),
    path('administracion_usuario/', views.administracion_usuarios, name='administracion_usuario'),
    path('nuevo_usuario/', views.nuevo_usuario, name='nuevo_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('list_usuario/', views.list_usuarios, name='list_usuario'),
    path('about/', views.about, name='about'),
    path('prediccion/', views.prediccion_view, name='prediccion'),
    path('simulacion/', views.simulacion_view, name='simulacion'),
    path('registros/', views.registros_almacenados, name='registros'),
    path('feedback/', views.enviar_feedback, name='enviar_feedback'),
    path('admin/feedback/', leer_feedback, name='leer_feedback'),
]