from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
<<<<<<< HEAD
from django.contrib import messages
from .models import recursos, gastos_recursos ,salud_gallinas
from .formularios import RecursoForm , GastoForm, SaludForm
=======
from .models import *
>>>>>>> 56afc465aff3921e18c22fac0a2fce58e76e9ce6
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
def recurso(request):
    recursos_list = recursos.objects.all()
    return render(request, 'adm-recursos.html',{'recursos_list': recursos_list})

@csrf_protect
@login_required
def contabilidad(request):
    return render(request, 'adm-contabilidad.html')


@csrf_protect
@login_required
def agregarGasto(request):
    formulario = GastoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('recurso')
    return render(request, 'adm-agregarGasto.html', {'formulario': formulario})

@csrf_protect
@login_required
def adicion(request):
    formulario = RecursoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, '¡Recurso Agregado con Exito!')   
        return redirect('recurso')
    return render(request, 'adm-adicion.html', {'formulario': formulario})



@csrf_protect
@login_required
def editarRecurso(request, id):
    recurso = recursos.objects.get(id=id)
    formulario = RecursoForm(request.POST or None, request.FILES or None, instance=recurso)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('recurso')
    return render(request, 'adm-editarRecurso.html', {'formulario': formulario})



@csrf_protect
@login_required
def eliminarRecurso(request, id):
    recurso_delete = get_object_or_404(recursos, id=id)
    recurso_delete.delete(using=None, keep_parents=False)
    messages.error(request,"Recurso Eliminado!")
    return redirect('recurso')

@csrf_protect
@login_required
def cuidado(request):
    return render(request, 'adm-cuidado.html')


