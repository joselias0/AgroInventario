from django import forms
from .models import Producto, Tamaño, productividad, ventas, recursos, gastos_recursos, salud_gallinas

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class TamañoForm(forms.ModelForm):
    class Meta:
        model = Tamaño
        fields = '__all__'

class ProductividadForm(forms.ModelForm):
    class Meta:
        model = productividad
        fields = '__all__'

class VentasForm(forms.ModelForm):
    class Meta:
        model = ventas
        fields = '__all__'


