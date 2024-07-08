from django.contrib import admin
from .models import MallaCurricular, Ciclo, Asignatura, PeriodoAcademico


# Register your models here.

admin.site.register(MallaCurricular)
admin.site.register(Ciclo)
admin.site.register(Asignatura)
admin.site.register(PeriodoAcademico)
