from django import forms
from .models import recursos , gastos_recursos, salud_gallinas

class RecursoForm(forms.ModelForm):
    class Meta:
        model = recursos
        fields = '__all__'


class GastoForm(forms.ModelForm):
    class Meta:
        model = gastos_recursos
        fields = ['precio', 'fecha', 'cantidad_agregada']


class SaludForm(forms.ModelForm):
    class Meta:
        model = salud_gallinas
        fields = ['tipo_accion', 'fecha', 'id_recurso', 'cantidad_recurso_usado', 'comentarios']

    # Modificar el campo id_recurso para que sea un ModelChoiceField
    id_recurso = forms.ModelChoiceField(queryset=recursos.objects.all(), empty_label=None)
