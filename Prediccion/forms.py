from django import forms

from Prediccion.models import MallaCurricular, Ciclo, Asignatura, PeriodoAcademico


class MallaCurricularForm(forms.ModelForm):
    class Meta:
        model = MallaCurricular
        fields = ['codigo', 'nombre_malla', 'tituloOtorgado']

        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip01', 'required': 'required'}),
            'nombre_malla': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip02', 'required': 'required'}),
            'tituloOtorgado': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip03', 'required': 'required'}),
        }


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        fields = ['nombre_ciclo']

        widgets = {
            'nombre_ciclo': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip04', 'required': 'required'}),
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['codigo_asignatura', 'nombre_asignatura']

        widgets = {
            'codigo_asignatura': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip05', 'required': 'required'}),
            'nombre_asignatura': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'validationTooltip06', 'required': 'required'}),
        }


class ExcelUploadForm(forms.Form):
    malla = forms.ModelChoiceField(
        queryset=MallaCurricular.objects.all(),
        label="Seleccione una Malla",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    archivo_excel = forms.FileField(
        label="Seleccione un archivo Excel",
        widget=forms.FileInput(attrs={'class': 'custom-file-input'})
    )


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = PeriodoAcademico
        fields = ['fecha_inicio', 'fecha_fin', 'desertores']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'desertores': forms.NumberInput(attrs={'class': 'form-control'}),
        }
