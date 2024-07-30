from django.contrib import admin
from .models import MallaCurricular, Ciclo, Asignatura, PeriodoAcademico, Historico, CustomUser, Historico_Periodo


# Register your models here.
class MallaCurricularAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre_malla', 'tituloOtorgado')
    search_fields = ('codigo', 'nombre_malla', 'tituloOtorgado')
    list_filter = ('nombre_malla', 'tituloOtorgado')
    ordering = ('id',)


class CicloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_ciclo', 'malla_curricular')
    search_fields = ('nombre_ciclo', 'malla_curricular')
    list_filter = ('nombre_ciclo', 'malla_curricular')
    ordering = ('id',)


class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_asignatura', 'nombre_asignatura', 'ciclo')
    search_fields = ('codigo_asignatura', 'nombre_asignatura', 'ciclo')
    list_filter = ('codigo_asignatura', 'nombre_asignatura', 'ciclo')
    ordering = ('id',)


class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_periodo', 'fecha_inicio', 'fecha_fin')
    search_fields = ('codigo_periodo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('codigo_periodo', 'fecha_inicio', 'fecha_fin')
    ordering = ('id',)


class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores', 'ciclo')
    search_fields = ('matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores', 'ciclo')
    list_filter = ('matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores', 'ciclo')
    ordering = ('id',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'role')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'role')
    ordering = ('id',)


class HistoricoPeriodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores')
    search_fields = ('matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores')
    list_filter = ('matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'periodo_academico', 'desertores')
    ordering = ('id',)


admin.site.register(MallaCurricular, MallaCurricularAdmin)
admin.site.register(Ciclo, CicloAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(PeriodoAcademico, PeriodoAcademicoAdmin)
admin.site.register(Historico, HistoricoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Historico_Periodo, HistoricoPeriodoAdmin)
