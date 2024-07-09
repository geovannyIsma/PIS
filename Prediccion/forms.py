from django import forms

from Prediccion.models import MallaCurricular, Ciclo, Asignatura


class MallaCurricularForm(forms.ModelForm):
    class Meta:
        model = MallaCurricular
        fields = ['codigo', 'nombre_malla', 'tituloOtorgado']

        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip01', 'required': 'required'}),
            'nombre_malla': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip02', 'required': 'required'}),
            'tituloOtorgado': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip03', 'required': 'required'}),
        }


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        fields = ['nombre_ciclo']

        widgets = {
            'nombre_ciclo': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip04', 'required': 'required'}),
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['codigo_asignatura', 'nombre_asignatura']

        widgets = {
            'codigo_asignatura': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip05', 'required': 'required'}),
            'nombre_asignatura': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationTooltip06', 'required': 'required'}),
        }