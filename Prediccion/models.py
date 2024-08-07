from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
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


class Historico(models.Model):
    matriculados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Matriculados")
    reprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Reprobados")
    abandonaron = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Abandonaron")
    aprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Aprobados")
    periodo_academico = models.ForeignKey('PeriodoAcademico', on_delete=models.CASCADE,verbose_name="Periodo Académico")
    desertores = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Desertores", default=0)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, verbose_name="Ciclo", default=1)

    class Meta:
        verbose_name = "Histórico"
        verbose_name_plural = "Históricos"

    def __str__(self):
        return f"{self.periodo_academico} - {self.ciclo} - {self.matriculados} - {self.reprobados} - {self.abandonaron} - {self.aprobados}"


class PeriodoAcademico(models.Model):
    codigo_periodo = models.CharField(max_length=50, default="", verbose_name="Código de Periodo")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")

    class Meta:
        verbose_name = "Periodo Académico"
        verbose_name_plural = "Periodos Académicos"

    def __str__(self):
        return self.codigo_periodo


class Historico_Periodo(models.Model):
    matriculados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Matriculados", default=0)
    reprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Reprobados", default=0)
    abandonaron = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Abandonaron", default=0)
    aprobados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Aprobados", default=0)
    desertores = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Desertores", default=0)
    periodo_academico = models.ForeignKey('PeriodoAcademico', on_delete=models.CASCADE,
                                          verbose_name="Periodo Académico")

    class Meta:
        verbose_name = "Histórico de Periodo"
        verbose_name_plural = "Históricos de Periodos"

    def __str__(self):
        return f"{self.periodo_academico} - {self.matriculados} - {self.reprobados} - {self.abandonaron} - {self.aprobados}"


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    CONSULTOR = 'consultor'
    PREDICTOR = 'predictor'

    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CONSULTOR, 'Consultor'),
        (PREDICTOR, 'Predictor')
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=CONSULTOR)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_consultor(self):
        return self.role == self.CONSULTOR

    def is_predictor(self):
        return self.role == self.PREDICTOR

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_superuser and not self.is_staff:
            if self.role == self.ADMIN:
                admin_group, created = Group.objects.get_or_create(name='Administrador')
                self.groups.add(admin_group)
            elif self.role == self.CONSULTOR:
                registered_group, created = Group.objects.get_or_create(name='Consultor')
                self.groups.add(registered_group)
            elif self.role == self.PREDICTOR:
                predictor_group, created = Group.objects.get_or_create(name='Predictor')
                self.groups.add(predictor_group)


class Feedback(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario")
    titulo = models.CharField(max_length=200)
    sugerencia = models.TextField()
    experiencia = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"{self.usuario} - {self.fecha_creacion}"