from django import forms
from .models import recursos , gastos_recursos, salud_gallinas

class RecursoForm(forms.ModelForm):
    class Meta:
        model = recursos
        fields = '__all__'

class GastoForm(forms.ModelForm):
    class Meta:
        model = gastos_recursos
        fields = '__all__'

class SaludForm(forms.ModelForm):
    class Meta:
        model = salud_gallinas
        fields = '__all__'