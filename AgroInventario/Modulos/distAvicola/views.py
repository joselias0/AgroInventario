from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from .models import *
# Create your views here.

@login_required
@csrf_protect
def salir(request):
    logout(request)
    return redirect('/')

@csrf_protect
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_protect
@login_required
def huevos(request):
    pro = Producto.objects.all()
    return render(request, 'adm-huevos.html', {'Producto':pro})

@csrf_protect
@login_required
def venta(request):
    return render(request, 'adm-ventas.html')

@csrf_protect
@login_required
def recursos(request):
    return render(request, 'adm-recursos.html')

@csrf_protect
@login_required
def contabilidad(request):
    return render(request, 'adm-contabilidad.html')

@csrf_protect
@login_required
def cuidado(request):
    return render(request, 'adm-cuidado.html')


