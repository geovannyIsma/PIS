from django.db import models


class MallaCurricular(models.Model):
    codigo = models.CharField(max_length=50, default="")
    nombre_malla = models.CharField(max_length=80)
    tituloOtorgado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.tituloOtorgado} - {self.codigo}"


class Ciclo(models.Model):
    nombre_ciclo = models.CharField(max_length=50)
    cantidad_asignaturas = models.IntegerField(default=0)
    malla_curricular = models.ForeignKey(MallaCurricular, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Asignatura(models.Model):
    codigo_asignatura = models.CharField(max_length=50)
    nombre_asignatura = models.CharField(max_length=100)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_asignatura


class Historico(models.Model):
    matriculados = models.IntegerField()
    reprobados = models.IntegerField()
    desertores = models.IntegerField()
    aprobados = models.IntegerField()
    aplazadores = models.IntegerField()
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo_academico = models.ForeignKey('PeriodoAcademico', on_delete=models.CASCADE)

    def __str__(self):
        return self.asignatura.nombre_asignatura


class PeriodoAcademico(models.Model):
    codigo_periodo = models.CharField(max_length=50, default="")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.codigo_periodo
