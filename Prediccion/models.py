from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator


class MallaCurricular(models.Model):
    codigo = models.CharField(max_length=50, default="", verbose_name="Código")
    nombre_malla = models.CharField(max_length=80, verbose_name="Nombre de la Malla")
    tituloOtorgado = models.CharField(max_length=100, verbose_name="Título Otorgado")

    class Meta:

        verbose_name = "Malla Curricular"
        verbose_name_plural = "Mallas Curriculares"

    def __str__(self):
        return f"{self.nombre_malla} - {self.tituloOtorgado} - {self.codigo}"


class Ciclo(models.Model):
    nombre_ciclo = models.CharField(max_length=50, verbose_name="Nombre del Ciclo")
    malla_curricular = models.ForeignKey(MallaCurricular, on_delete=models.CASCADE, verbose_name="Malla Curricular")

    class Meta:
        verbose_name = "Ciclo"
        verbose_name_plural = "Ciclos"

    def __str__(self):
        return self.nombre_ciclo


class Asignatura(models.Model):
    codigo_asignatura = models.CharField(max_length=50, verbose_name="Código de Asignatura", unique=True)
    nombre_asignatura = models.CharField(max_length=100, verbose_name="Nombre de Asignatura")
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, verbose_name="Ciclo")

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

    def __str__(self):
        return self.nombre_asignatura


class Historico(models.Model):
    matriculados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Matriculados")
    reprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Reprobados")
    desertores = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Desertores")
    aprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Aprobados")
    aplazadores = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Aplazadores")
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, verbose_name="Asignatura")
    periodo_academico = models.ForeignKey('PeriodoAcademico', on_delete=models.CASCADE, verbose_name="Periodo Académico")

    class Meta:
        verbose_name = "Histórico"
        verbose_name_plural = "Históricos"

    def __str__(self):
        return f"{self.asignatura.nombre_asignatura} - {self.periodo_academico.codigo_periodo}"


class PeriodoAcademico(models.Model):
    codigo_periodo = models.CharField(max_length=50, default="", verbose_name="Código de Periodo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")

    class Meta:
        verbose_name = "Periodo Académico"
        verbose_name_plural = "Periodos Académicos"

    def __str__(self):
        return self.codigo_periodo
