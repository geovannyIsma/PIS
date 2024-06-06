from django import forms

class SEIRForm(forms.Form):
    M = forms.IntegerField(label='Matriculados', min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}))
    A0 = forms.IntegerField(label='Aprobados', min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}))
    R0 = forms.IntegerField(label='Reprobados', min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}))
    D0 = forms.IntegerField(label='Desertores', min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}))
    days = forms.IntegerField(label='Días', min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control border-2 rounded-pill'}))

