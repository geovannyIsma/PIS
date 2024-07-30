from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from Prediccion.models import MallaCurricular, Ciclo, PeriodoAcademico, CustomUser, Historico_Periodo


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
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    email = forms.EmailField(max_length=254, required=True, help_text='Requerido. Ingrese una dirección de correo válida.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active')


class HistoricoPeriodoForm(forms.ModelForm):
    class Meta:
        model = Historico_Periodo
        fields = ['matriculados', 'reprobados', 'abandonaron', 'aprobados', 'desertores']
        widgets = {
            'matriculados': forms.NumberInput(attrs={'class': 'form-control'}),
            'reprobados': forms.NumberInput(attrs={'class': 'form-control'}),
            'abandonaron': forms.NumberInput(attrs={'class': 'form-control'}),
            'aprobados': forms.NumberInput(attrs={'class': 'form-control'}),
            'desertores': forms.NumberInput(attrs={'class': 'form-control'}),
        }