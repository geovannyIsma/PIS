from django import forms

from Prediccion.models import MallaCurricular, Ciclo, Asignatura


class MallaCurricularForm(forms.ModelForm):
    class Meta:
        model = MallaCurricular
        fields = ['codigo', 'nombre_malla', 'tituloOtorgado']


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        fields = ['nombre_ciclo']


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['codigo_asignatura', 'nombre_asignatura']

